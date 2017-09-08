import json
import logging
import socket
import subprocess
import time
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta

from celery import states
from celery.exceptions import Ignore
from celery.task import (
    PeriodicTask,
    Task,
)
from django.core.files.base import ContentFile

from .models import (
    Epiphan,
    EpiphanSource,
    Export,
    Recorder,
    Recording,
)

logger = logging.getLogger(__name__)

# Metadata:
# ffprobe -v quiet -print_format json -show_format -show_streams Recorder_Aug07_12-56-01.ts

# Side-by-Side:
# ffmpeg -i Recorder_Aug07_12-56-01.ts -filter_complex "[i:0x100][i:0x102]hstack=inputs=2[v];[i:0x101][i:0x103]amerge[a]" -map "[v]" -map "[a]" -ac 2 output.mp4"

# Split video in two:
# ffmpeg -i output.mp4 -filter_complex "[0:v]crop=iw/2:ih:0:0[left];[0:v]crop=iw/2:ih:iw/2:0[right]" -map "[left]" left.mp4 -map "[right]" right.mp4


class ProcessRecordingTask(Task):

    def run(self, pk, **kwargs):
        logger.debug('Processing recording: {}'.format(pk))
        rec = Recording.objects.get(pk=pk)
        probe = subprocess.run(
            [
                'ffprobe',
                '-v',
                'quiet',
                '-print_format',
                'json',
                '-show_format',
                '-show_streams',
                rec.data.path
            ],
            stdout=subprocess.PIPE
        )
        info = probe.stdout.decode('utf-8')
        logger.debug('Extracted metadata: {}'.format(info))
        rec.info = json.loads(info)
        rec.save()
        logger.info('Finished recording: {}'.format(pk))


class EpiphanProvisionTask(Task):

    def run(self, pk):
        epiphan = Epiphan.objects.get(pk=pk)
        epiphan.session.post(
            epiphan.url.path('admin/afucfg').as_string(),
            data={
                'pfd_form_id': 'fn_afu',
                'afuEnable': 'on',
                'afuProtocol': 'sftp',
                'afuInterval': 0,
                'afuRemotePath': '',
                'remove-source-files': 'on',
                'mark-downloaded': None,
                'ftpServer': None,
                'ftpPort': None,
                'ftpuser': None,
                'ftppasswd': None,
                'ftptmpfile': None,
                'cifsPort': None,
                'cifsServer': None,
                'cifsShare': None,
                'cifsDomain': None,
                'cifsUser': None,
                'cifsPasswd': None,
                'cifstmpfile': None,
                'rsyncServer': None,
                'rsyncModule': None,
                'rsyncUser': None,
                'rsyncPassword': None,
                'rsyncChecksum': None,
                'scpServer': None,
                'scpPort': None,
                'scpuser': None,
                'scppasswd': None,
                'sftpServer': epiphan.server.hostname or socket.getfqdn(),
                'sftpPort': epiphan.server.port,
                'sftpuser': epiphan.pk,
                'sftppasswd': None,
                'sftptmpfile': None,
                's3Region': None,
                's3Bucket': None,
                's3Key': None,
                's3Secret': None,
                's3Token': None,
                'preserve-channel-name': None,
            }
        )
        epiphan.session.post(
            epiphan.url.path('admin/sshkeys.cgi').as_string(),
            files={
                'identity': (
                    'key',
                    epiphan.private_key
                )
            },
            data={
                'command': 'add',
            }
        )


class ExportTask(Task):

    def run(self, pk, exporter):
        classes = Export.__subclasses__()
        exporters = {c.__name__: c for c in classes}
        if exporter not in exporters:
            self.update_state(
                state=states.FAILURE,
                meta='Unknown exporter: {}'.format(exporter)
            )
            raise Ignore()
        try:
            rec = Recording.objects.get(pk=pk)
        except Recodring.DoesNotExists:
            self.update_state(
                state=states.FAILURE,
                meta='Unknown recording: {}'.format(pk)
            )
            raise Ignore()
        cls = exporters.get(exporter)
        logger.info('Recording {} export requested: {}'.format(rec.pk, cls))
        (inst, _) = cls.objects.get_or_create(recording=rec)
        if not inst.data:
            logger.info('Recording {} processing: {}'.format(rec.pk, cls))
            inst.process(self.progress)
            logger.debug('Recording {} download URL: {}'.format(rec.pk, inst.data.url))
        return inst.data.url

    def progress(self, action, current, maximum):
        logger.debug('Progress: {} {}/{}'.format(action, current, maximum))
        self.update_state(
            state='PROGRESS',
            meta={
                'action': action,
                'current': current,
                'maximum': maximum,
            }
        )


class RecorderOnlineTask(PeriodicTask):
    run_every = timedelta(minutes=5)

    def run(self, **kwargs):

        def check(recorder):
            logger.debug('Pinging {}.'.format(recorder))
            proc = subprocess.run(
                [
                    'ping',
                    '-c1',
                    '-w2',
                    recorder.hostname
                ]
            )
            online = (proc.returncode == 0)
            if recorder.online != online:
                recorder.online = online
                logger.debug('Recorder {} online: {}'.format(recorder, online))
                recorder.save()

        recorders = Recorder.objects.filter(enabled=True)
        logger.info('Pinging {} recorders.'.format(recorders.count()))

        with ThreadPoolExecutor() as executor:
            executor.map(check, recorders)


class EpiphanPreviewTask(PeriodicTask):
    run_every = timedelta(minutes=10)

    def run(self, **kwargs):

        def update(source):
            try:
                print(source)
                #logger.info('Taking preview image from {}.'.format(epiphan))
                path = 'api/channels/{s.number}/preview'.format(s=source)
                print(path)
                url = source.epiphan.url.path(path).as_string()
                print(url)
                logger.info('Retrieving {}'.format(url))
                r = source.epiphan.session.get(url)
                print(r)
                source.preview.save('preview.jpg', ContentFile(r.content))
            except Exception as e:
                logger.warn(e)

        sources = EpiphanSource.objects.filter(
            epiphan__enabled=True,
            epiphan__online=True,
        )
        logger.info('Updating previews on {} sources.'.format(sources.count()))

        with ThreadPoolExecutor() as executor:
            executor.map(update, sources)
