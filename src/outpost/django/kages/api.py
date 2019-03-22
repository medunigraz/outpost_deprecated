import logging

import ldap
from rest_framework import (
    exceptions,
    permissions,
    viewsets,
)
from rest_framework.response import Response

from . import models
from .conf import settings

logger = logging.getLogger(__name__)


class TranslateViewSet(viewsets.ViewSet):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def list(self, request):
        return Response()

    def retrieve(self, request, pk=None):
        if not pk:
            return Response(False)
        try:
            conn = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
            conn.simple_bind_s(
                settings.AUTH_LDAP_BIND_DN,
                settings.AUTH_LDAP_BIND_PASSWORD
            )
            result = conn.search_s(
                settings.AUTH_LDAP_USER_SEARCH.base_dn,
                settings.AUTH_LDAP_USER_SEARCH.scope,
                settings.KAGES_PERS_ID_FILTER.format(id=int(pk)),
                settings.KAGES_PERS_FIELDS
            )
            found = len(result) == 1
        except Exception as e:
            logger.warn(
                f'LDAP query failed when matching KAGes ID: {e}'
            )
            found = False
        logger.debug(f'Matched KAGes ID: {found}')
        return Response({'exists': found})
