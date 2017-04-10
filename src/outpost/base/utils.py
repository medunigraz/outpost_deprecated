from uuid import uuid4
from pathlib import PurePosixPath
from base64 import urlsafe_b64encode


class Uuid4Upload(object):

    def __init__(self, instance, filename):
        f = PurePosixPath(filename)
        u = urlsafe_b64encode(uuid4().bytes).decode('ascii').rstrip('=')
        p = PurePosixPath(instance.__module__, instance._meta.object_name)
        self.path = p.joinpath(u).with_suffix(f.suffix).as_posix()

    def __unicode__(self):
        return self.path
