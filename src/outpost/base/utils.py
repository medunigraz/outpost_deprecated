from base64 import urlsafe_b64encode
from pathlib import PurePosixPath
from uuid import uuid4
import subprocess
import logging

from functools import partial


logger = logging.getLogger(__name__)


class Uuid4Upload(str):

    def __new__(cls, instance, filename):
        f = PurePosixPath(filename)
        u = urlsafe_b64encode(uuid4().bytes).decode('ascii').rstrip('=')
        p = PurePosixPath(instance.__module__, instance._meta.object_name)
        return str.__new__(cls, p.joinpath(u).with_suffix(f.suffix))


def colorscale(hexstr, scalefactor):
    """
    Scales a hex string by ``scalefactor``. Returns scaled hex string.

    To darken the color, use a float value between 0 and 1.
    To brighten the color, use a float value greater than 1.

    >>> colorscale("DF3C3C", .5)
    6F1E1E
    >>> colorscale("52D24F", 1.6)
    83FF7E
    >>> colorscale("4F75D2", 1)
    4F75D2
    """

    def clamp(val, minimum=0, maximum=255):
        if val < minimum:
            return minimum
        if val > maximum:
            return maximum
        return val

    if scalefactor < 0 or len(hexstr) != 6:
        return hexstr

    r, g, b = int(hexstr[:2], 16), int(hexstr[2:4], 16), int(hexstr[4:], 16)

    r = int(clamp(r * scalefactor))
    g = int(clamp(g * scalefactor))
    b = int(clamp(b * scalefactor))

    return "%02x%02x%02x" % (r, g, b)


class Process():

    def __init__(self, *args):
        self.handlers = []
        logger.debug('Preparing: {}'.format(' '.join(args)))
        self.cmd = partial(
            subprocess.Popen,
            args,
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

            logger.debug('Process line: {}'.format(line))
            for h in self.handlers:
                h(line)
        return pipe.returncode
