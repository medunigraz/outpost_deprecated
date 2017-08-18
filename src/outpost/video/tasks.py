import time
import json
import logging
import subprocess
from concurrent import futures
from datetime import timedelta

from celery import states
from celery.task import Task
from celery.exceptions import Ignore

from .models import Recording, Export

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
                "ffprobe",
                "-v",
                'quiet',
                '-print_format',
                'json',
                '-show_format',
                '-show_streams',
                rec.data.path
            ],
            stdout=subprocess.PIPE
        )
        info = json.loads(probe.stdout)
        rec.info = info
        rec.save()
        logger.info('Finished recording: {}'.format(pk))


class DebugTask(Task):

    def run(self):
        for i in range(100):
            self.update_state(
                state='PROGRESS',
                meta={
                    'current': i,
                    'total': 100
                }
            )
            time.sleep(2)
        print('Debug task running')
        return 1234


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

    def progress(self, current, maximum):
        logger.debug('Progress: {}/{}'.format(current, maximum))
        self.update_state(
            state='PROGRESS',
            meta={
                'current': current,
                'maximum': maximum,
            }
        )
