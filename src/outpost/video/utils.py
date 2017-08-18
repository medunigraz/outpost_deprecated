import re
import math
import subprocess


class FFMPEGProcess(object):

    re_duration = re.compile('Duration: (\d{2}):(\d{2}):(\d{2}).(\d{2})[^\d]*', re.U)
    re_position = re.compile('time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})\d*', re.U | re.I)

    def __init__(self, command, status_handler=None):

        def time2sec(search):
            return sum([i**(2-i) * int(search.group(i+1)) for i in range(3)])

        pipe = subprocess.Popen(
            ['ffmpeg', '-y'] + command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        duration = None
        position = None
        current = 0

        while True:
            line = pipe.stdout.readline().strip()

            if line == '' and pipe.poll() is not None:
                break

            if duration is None:
                duration_match = self.re_duration.match(line)
                if duration_match:
                    duration = time2sec(duration_match)
            else:
                position_match = self.re_position.search(line)
                if position_match:
                    new = time2sec(position_match)
                    if new > current:
                        if callable(status_handler):
                            status_handler(new, duration)
                        current = new
