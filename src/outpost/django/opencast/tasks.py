import logging
from datetime import timedelta

import ldap
import requests
from celery.task import (
    PeriodicTask,
    Task,
)
from django.core.cache import cache
from purl import URL

from .conf import settings
from .models import GroupMap

logger = logging.getLogger(__name__)


class GroupMapDispachterTask(PeriodicTask):
    run_every = timedelta(hours=1)

    def run(self, **kwargs):
        for gm in GroupMap.objects.filter(enabled=True):
            GroupMapTask().delay(gm.pk)


class GroupMapTask(Task):
    url = URL(settings.OPENCAST_API_BASE)

    def __init__(self):
        self.session = requests.Session()
        self.session.auth = (
            settings.OPENCAST_API_USERNAME,
            settings.OPENCAST_API_PASSWORD
        )
        self.session.headers.update({
            'accept': 'application/json'
        })

    def run(self, pk, **kwargs):
        lock = cache.lock(f'opencast-groupmap-{pk}')
        if not lock.acquire(blocking=False):
            logger.warn(f'Processing {lock.name} already locked, aborting')
            return
        try:
            self.process(pk)
        finally:
            lock.release()

    def process(self, pk):
        gm = GroupMap.objects.get(pk=pk)
        try:
            resp = self.session.get(
                self.url.path(f'api/v1/groups/{gm.group.lower()}')
            )
            resp.raise_for_status()
            oc_group = resp.json()
        except Exception as e:
            logger.warn(f'Failed to fetch Opencast group {gm}: {e}')
            return
        try:
            conn = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
            conn.simple_bind_s(
                settings.AUTH_LDAP_BIND_DN,
                settings.AUTH_LDAP_BIND_PASSWORD
            )
            result = conn.search_s(
                gm.dn,
                settings.AUTH_LDAP_USER_SEARCH.scope,
                f'(&({gm.username_field}=*)({gm.email_field}=*){gm.filter})',
                [gm.username_field, gm.email_field]
            )

            def convert_result(user):
                return (
                    user.get(gm.username_field).pop().decode('utf-8'),
                    user.get(gm.email_field).pop().decode('utf-8')
                )

            ldap_group = dict(convert_result(user) for dn, user in result)
        except ldap.LDAPError as e:
            logger.warn(
                'LDAP query failed when synchronizing Opencast users '
                f'for {gm}: {e}'

            )
            return

        update = set()
        create = set()
        for username, email in ldap_group.items():
            logger.debug(f'Checking external user {username} with {email}')
            try:
                user_external = self.get_user_external(username)
            except requests.HTTPError as e:
                if e.status == 404:
                    create.add(username)
                else:
                    raise
            except Exception as e:
                logger.warn(f'Failed to fetch details for external user {username}: {e}')
                continue
            logger.debug(f'Fetched external user data for {username}: {user_external}')
            if user_external.get('email') != email:
                update.add(username)
            logger.debug(f'Checking internal user {username} with {email}')
            try:
                user_internal = self.get_user_internal(username)
            except Exception as e:
                logger.warn(f'Failed to fetch details for internal user {username}: {e}')
                update.add(username)
                continue
            logger.debug(f'Fetched internal _user data for {username}: {user_internal}')
            if user_internal.get('email') != email:
                update.add(username)
        members = set(oc_group.get('members'))
        for username in create:
            logger.info(f'Creating missing user {username}')
            try:
                self.create_user_external(username)
                members.add(username)
            except Exception as e:
                logger.warn(f'Failed to create user {username}: {e}')
                continue
        for d in members.difference(set(ldap_group.keys())):
            logger.debug(f'Remove deprecated user from {gm}: {d}')
            members.remove(d)
        for d in update:
            logger.debug(f'Remove mismatching user from {gm}: {d}')
            if d in members:
                members.remove(d)
        logger.debug(f'Updating group {gm} with deprecated and mismatched users removed')
        try:
            self.update_group(
                oc_group.get('name'),
                oc_group.get('roles') or [oc_group.get('role')],
                list(members)
            )
        except Exception as e:
            logger.warn(f'Failed to update group {gm}: {e}')
            return
        logger.debug(f'Updating users')
        for username in update:
            logger.info(f'Updating user {username}')
            try:
                logger.debug(f'Removing external user {username}')
                self.remove_user_external(username)
                logger.debug(f'Creating external user {username}')
                self.create_user_external(username)
                members.add(username)
            except Exception as e:
                logger.warn(f'Failed to update {username}: {e}')
                continue
        logger.debug(f'Updating group {gm}')
        try:
            self.update_group(
                oc_group.get('name'),
                oc_group.get('roles') or [oc_group.get('role')],
                list(members)
            )
        except Exception as e:
            logger.warn(f'Failed to update group {gm}: {e}')
            return

    def update_group(self, name, roles, members):
        resp = self.session.put(
            self.url.path(f'api/v1/groups/{name.lower()}').as_string(),
            json={
                'name': name,
                'roles': roles,
                'members': members
            }
        )
        resp.raise_for_status()

    def get_user_external(self, username):
        provider = settings.OPENCAST_LDAP_PROVIDER
        path = f'api/v1/users/providers/{provider}/users/{username}'
        resp = self.session.get(
            self.url.path(path).as_string()
        )
        resp.raise_for_status()
        return resp.json()

    def get_user_internal(self, username):
        path = f'api/v1/users/users/{username}'
        resp = self.session.get(
            self.url.path(path).as_string()
        )
        resp.raise_for_status()
        return resp.json()

    def create_user_external(self, username):
        resp = self.session.post(
            self.url.path('api/v1/users/external').as_string(),
            json={
                'username': username,
                'provider': settings.OPENCAST_LDAP_PROVIDER,
                'roles': []
            }
        )
        resp.raise_for_status()
        return resp.json()

    def remove_user_external(self, username):
        provider = settings.OPENCAST_LDAP_PROVIDER
        path = f'api/v1/users/providers/{provider}/users/{username}'
        resp = self.session.delete(
            self.url.path(path).as_string()
        )
        resp.raise_for_status()

    def remove_user_internal(self, username):
        path = f'api/v1/users/internal/users/{username}'
        resp = self.session.delete(
            self.url.path(path).as_string()
        )
        resp.raise_for_status()
