import asyncio
import logging
import os
import sys
from datetime import datetime
from functools import partial, wraps
from pathlib import Path

import asyncssh
from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from django.core.files.base import ContentFile

from ...models import (Epiphan, Server, Recording)
from ...tasks import ProcessRecordingTask

logger = logging.getLogger(__name__)


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug('Call: {}'.format(func.__name__))
        try:
            result = func(*args, **kwargs)
            logger.debug('Return: {}: {}'.format(func.__name__, result))
            return result
        except Exception as e:
            print('Exception', e)
    return wrapper


class SSHServer(asyncssh.SSHServer):

    def __init__(self, server):
        self._server = server

    def connection_made(self, conn):
        logger.debug('Got connection from {}'.format(conn))
        self._conn = conn

    def begin_auth(self, username):
        logger.debug('User: {}'.format(username))
        cond = {
            'pk': username,
            'server': self._server,
            'active': True,
        }
        device = Epiphan.objects.get(**cond)
        logger.debug('Device: {}'.format(device))
        private = asyncssh.import_private_key(device.key.tobytes())
        public = private.export_public_key().decode('ascii')
        logger.debug('Public key: {}'.format(public))

        key = asyncssh.import_authorized_keys(public)

        self._conn.set_authorized_keys(key)
        return True

    def public_key_auth_supported(self):
        return True

    def password_auth_supported(self):
        return False

    def kbdint_auth_supported(self):
        return False


class SFTPServer(asyncssh.SFTPServer):

    def __init__(self, server, conn):
        username = conn.get_extra_info('username')
        self._server = server
        self._epiphan = Epiphan.objects.get(pk=username)
        super().__init__(conn)
        unsupported = [
            'read',
            'rename',
            'posix_rename',
            'remove',
            'readlink',
            'readlink',
            'link',
            'lstat',
            'fstat',
            'setstat',
            'fsetstat',
            'statvfs',
            'fstatvfs',
            'listdir',
            'mkdir',
            'rmdir',
        ]
        for f in unsupported:
            setattr(self, f, partial(self.unsupported, f))

    def format_user(self, uid):
        return str(self._epiphan.pk)

    def format_group(self, gid):
        return str(self._epiphan.pk)

    def open(self, raw, pflags, attrs):
        path = Path(raw.decode('utf-8'))
        logger.info('Uploading video: {}'.format(path.name))
        rec = Recording(
            recorder=self._epiphan,
            info={}
        )
        rec.data.save(path.name, ContentFile(b''))
        if not rec.data.file.closed:
            rec.data.file.close()
        rec.data.file.open('wb')
        rec.save()
        return rec

    def close(self, rec):
        logger.info('Finished file: {}'.format(rec.data.path))
        if not rec.data.file.closed:
            rec.data.file.close()
        rec.save()
        ProcessRecordingTask.delay(rec.pk)

    def write(self, rec, offset, data):
        logger.debug(
            'Writing {} bytes of data at offset {}'.format(
                len(data),
                offset
            )
        )
        rec.data.file.seek(offset)
        written = rec.data.file.write(data)
        logger.info('Wrote {} bytes'.format(written))
        return written

    def fstat(self, rec):
        now = int(datetime.timestamp(datetime.now()))
        return asyncssh.SFTPAttrs(
            size=rec.data.file.size,
            uid=0,
            gid=0,
            permissions=int('100600', 8),
            atime=now,
            mtime=now,
            nlink=1
        )

    def stat(self, path):
        if path != b'/':
            raise asyncssh.SFTPError(
                asyncssh.FX_NO_SUCH_FILE,
                'no such file'
            )
        now = int(datetime.timestamp(datetime.now()))
        return asyncssh.SFTPAttrs(
            size=216,
            uid=0,
            gid=0,
            permissions=int('40755', 8),
            atime=now,
            mtime=now,
            nlink=1
        )

    def realpath(self, path):
        return b'/'

    def listdir(self, path):
        return [b'.', b'..']

    def unsupported(self, n, *args):
        print(n, args)
        raise asyncssh.SFTPError(
            asyncssh.FX_OP_UNSUPPORTED,
            'This server supports upload only!'
        )


class Command(BaseCommand):
    help = 'Runs the video upload SFTP server.'

    def add_arguments(self, parser):
        parser.add_argument('server', nargs='*', type=int)

    def handle(self, *args, **options):

        loop = asyncio.get_event_loop()

        async def start_server(server):
            self.stdout.write(self.style.SUCCESS('Starting server on {s.hostname}:{s.port}'.format(s=server)))
            await asyncssh.create_server(
                host=server.hostname,
                port=server.port,
                server_factory=partial(SSHServer, server),
                sftp_factory=partial(SFTPServer, server),
                server_host_keys=[
                    asyncssh.import_private_key(server.key.tobytes())
                ],
                x11_forwarding=False,
                agent_forwarding=False,
                login_timeout=10
            )

        cond = {
            'active': True
        }
        if options['server']:
            cond['pk__in'] = options['server']

        tasks = [start_server(s) for s in Server.objects.filter(**cond)]

        try:
            loop.run_until_complete(asyncio.gather(*tasks))
        except (OSError, asyncssh.Error) as exc:
            sys.exit('Error starting server: ' + str(exc))

        loop.run_forever()
