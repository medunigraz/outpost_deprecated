import logging
import math
import re
import subprocess

from functools import partial

logger = logging.getLogger(__name__)


class FFMPEGProcess():

    def __init__(self, command):
        self.handlers = []
        self.cmd = partial(
            subprocess.Popen,
            ['ffmpeg', '-y'] + command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

    def handler(self, h):
        if callable(h):
            self.handlers.append(h)

    def run(self):
        pipe = self.cmd()

        duration = None
        position = None
        current = 0

        while True:
            line = pipe.stdout.readline().strip()

            if line == '' and pipe.poll() is not None:
                break

            for h in self.handlers:
                logger.debug('Handling line: {}'.format(line))
                h(line)


class FFMPEGDurationHandler():
    duration = None
    current = 0
    re_duration = re.compile('Duration: (\d{2}):(\d{2}):(\d{2}).(\d{2})[^\d]*', re.U)
    re_position = re.compile('time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})\d*', re.U | re.I)

    def __init__(self, func):
        self.func = func

    def __call__(self, line):
        def time2sec(search):
            return sum([i**(2-i) * int(search.group(i+1)) for i in range(3)])

        if self.duration is None:
            duration_match = self.re_duration.match(line)
            if duration_match:
                self.duration = time2sec(duration_match)
        else:
            position_match = self.re_position.search(line)
            if position_match:
                new = time2sec(position_match)
                if new > self.current:
                    if callable(self.func):
                        self.func(new, self.duration)
                    self.current = new


class FFMPEGSceneHandler():

    def __init__(self, func):
        self.func = func

    def __call__(self, line):
        return


class FFProbeProcess():

    def __init__(self, command):

        self.cmd = partial(
            subprocess.run,
            [
                'ffprobe',
                '-v',
                'quiet',
                '-print_format',
                'json',
            ] + command,
            stdout=subprocess.PIPE
        )

    def run(self):
        info = probe.stdout.decode('utf-8')
        logger.debug('Extracted metadata: {}'.format(info))
        return json.loads(info)
