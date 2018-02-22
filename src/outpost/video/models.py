import logging
import os
import re
import shutil
import time
import uuid
from base64 import (
    b64encode,
    urlsafe_b64encode,
)
from decimal import Decimal
from functools import partial
from hashlib import (
    md5,
    sha256,
)
from io import StringIO
from pathlib import Path
from statistics import mean
from tempfile import (
    NamedTemporaryFile,
    TemporaryDirectory,
)
from uuid import uuid4
from zipfile import ZipFile

import asyncssh
import requests
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import (
    ArrayField,
    JSONField,
)
from django.core.cache import cache
from django.core.files import File
from django.core.files.images import ImageFile
from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from django_fsm import (
    FSMField,
    transition,
)
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from lxml import etree
from memoize import (
    delete_memoized,
    memoize,
)
from polymorphic.models import PolymorphicModel
from purl import URL
from requests import (
    Request,
    Session,
    codes,
)
from requests_toolbelt import MultipartEncoder
from taggit.managers import TaggableManager

from ..base.decorators import signal_connect
from ..base.models import NetworkedDeviceMixin
from ..base.utils import (
    Process,
    Uuid4Upload,
)
from .utils import (
    FFMPEGProgressHandler,
    FFProbeProcess,
)

logger = logging.getLogger(__name__)


@signal_connect
class Server(models.Model):
    hostname = models.CharField(max_length=128, blank=True)
    port = models.PositiveIntegerField(default=2022)
    key = models.BinaryField(null=False)
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = (
            ('hostname', 'port'),
        )
        ordering = (
            'hostname',
            'port',
        )

    def fingerprint(self):
        if not self.key:
            return None
        k = asyncssh.import_private_key(self.key.tobytes())
        d = sha256(k.get_ssh_public_key()).digest()
        f = b64encode(d).replace(b'=', b'').decode('utf-8')
        return 'SHA256:{}'.format(f)

    def pre_save(self, *args, **kwargs):
        if self.key:
            return
        pk = asyncssh.generate_private_key('ssh-rsa')
        self.key = pk.export_private_key()

    def ping(self):
        cache.set(
            'outpost-video-server-{}'.format(str(self)),
            True,
            timeout=10
        )

    @property
    def active(self):
        return cache.get(
            'outpost-video-server-{}'.format(str(self)),
            False
        )

    def __str__(self):
        if self.hostname:
            return '{s.hostname}:{s.port}'.format(s=self)
        return '*:{s.port}'.format(s=self)


class Recorder(NetworkedDeviceMixin, PolymorphicModel):
    name = models.CharField(max_length=128, blank=False, null=False)
    room = models.ForeignKey(
        'geo.Room',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    notifications = GenericRelation(
        'base.Notification'
    )
    retention = models.DurationField(
        default=None,
        null=True,
        blank=True
    )

    class Meta:
        ordering = (
            'name',
            'hostname',
        )
        permissions = (
            ('view_recorder', _('View Recorder')),
        )

    def __str__(self):
        return self.name


@signal_connect
class Epiphan(Recorder):
    username = models.CharField(max_length=128, blank=False, null=False)
    password = models.CharField(max_length=128, blank=False, null=False)
    server = models.ForeignKey(
        'Server',
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    key = models.BinaryField(null=False)
    provision = models.BooleanField(default=False)

    def fingerprint(self):
        if not self.key:
            return None
        k = asyncssh.import_private_key(self.key.tobytes())
        d = md5(k.get_ssh_public_key()).hexdigest()
        return ':'.join(a + b for a, b in zip(d[::2], d[1::2]))

    def private_key(self):
        return self.key.tobytes().decode('ascii')

    def post_init(self, *args, **kwargs):
        self.session = requests.Session()
        if self.username and self.password:
            self.session.auth = (self.username, self.password)
        self.url = URL(
            scheme='http',
            host=self.hostname,
            path='/'
        )

    def pre_save(self, *args, **kwargs):
        if self.key:
            return
        pk = asyncssh.generate_private_key('ssh-rsa', comment=self.name)
        # For compatibility with older SSH implementations
        self.key = pk.export_private_key('pkcs1-pem')
        self.save()

    def post_save(self, *args, **kwargs):
        if not self.online:
            return
        if self.provision:
            from .tasks import EpiphanProvisionTask
            EpiphanProvisionTask().run(self.pk)

    def reboot(self):
        url = self.url.path('admin/reboot.cgi').as_string()
        logger.info('Requesting reboot: {}'.format(url))
        self.session.get(url)
        self.online = False
        self.save()


@signal_connect
class EpiphanChannel(models.Model):
    epiphan = models.ForeignKey(
        'Epiphan',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=128)
    path = models.CharField(max_length=10)

    class Meta:
        ordering = (
            'name',
        )

    def request(self, key, value=None):
        m = value and 'set' or 'get'
        path = 'admin/{s.path}/{m}_params.cgi'.format(s=self, m=m)
        url = self.epiphan.url.path(path).query_param(key, value).as_string()
        try:
            r = self.epiphan.session.get(url)
        except Exception as e:
            logger.warn(e)
            return None
        else:
            delete_memoized(self.recording)
            return r

    def start(self):
        if self.recording():
            return
        logger.info('Starting recording for {s}'.format(s=self))
        self.request('rec_enabled', 'on')

    def stop(self):
        if not self.recording():
            return
        logger.info('Stopping recording for {s}'.format(s=self))
        self.request('rec_enabled', 'off')

    @memoize(timeout=10)
    def recording(self):
        if not self.epiphan.online:
            return False
        r = self.request('rec_enabled', '')
        if not r:
            return False
        return re.match('^rec_enabled = on$', r.text) is not None

    def response(self):
        data = dict()
        data['recording'] = self.recording()
        return data

    def __str__(self):
        return '{s.epiphan}, {s.name}'.format(s=self)

    def __repr__(self):
        return '{s.__class__.__name__}({s.pk})'.format(s=self)


class EpiphanSource(models.Model):
    epiphan = models.ForeignKey(
        'Epiphan',
        on_delete=models.CASCADE
    )
    number = models.PositiveSmallIntegerField()
    video = ProcessedImageField(
        upload_to=Uuid4Upload,
        format='JPEG',
        options={'quality': 60},
        null=True,
        blank=True
    )
    port = models.PositiveIntegerField(default=554)
    audio = ProcessedImageField(
        upload_to=Uuid4Upload,
        format='JPEG',
        options={'quality': 60},
        null=True,
        blank=True
    )
    input = models.ForeignKey(
        'Input',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = (
            'number',
        )

    def pre_delete(self, *args, **kwargs):
        self.video.delete(False)
        self.audio.delete(False)

    def update(self):
        rtsp = 'rtsp://{s.epiphan.hostname}:{s.port}/stream.sdp'.format(s=self)

        # Video preview
        try:
            args = [
                'ffmpeg',
                '-y',
                '-i',
                rtsp,
                '-frames:v',
                '1',
            ]
            with NamedTemporaryFile(suffix='.jpg') as output:
                args.append(output.name)
                ffmpeg = Process(*args)
                ffmpeg.run()
                self.video.delete(False)
                self.video.save(output.name, ImageFile(output))
        except Exception as e:
            logger.warn(e)

        # Audio waveform
        try:
            args = [
                'ffmpeg',
                '-y',
                '-t',
                '5',
                '-i',
                rtsp,
                '-filter_complex',
                'showwavespic=s=1280x240',
                '-frames:v',
                '1',
            ]
            with NamedTemporaryFile(suffix='.png') as output:
                args.append(output.name)
                ffmpeg = Process(*args)
                ffmpeg.run()
                self.audio.delete(False)
                self.audio.save(output.name, ImageFile(output))
        except Exception as e:
            logger.warn(e)

    def __str__(self):
        return '{s.epiphan}, {s.number}'.format(s=self)


class Input(PolymorphicModel):
    name = models.CharField(max_length=128, blank=False, null=False)


class PanasonicCamera(NetworkedDeviceMixin, Input):
    pass


@signal_connect
class Recording(TimeStampedModel):
    recorder = models.ForeignKey(
        'Recorder',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    data = models.FileField(
        upload_to=Uuid4Upload
    )
    info = JSONField(null=True)

    class Meta:
        ordering = (
            '-created',
        )
        permissions = (
            ('view_recording', _('View Recording')),
        )

    def pre_delete(self, *args, **kwargs):
        self.data.delete(False)

    def __str__(self):
        return 'Recorded by {s.recorder} on {s.modified}'.format(s=self)


class EpiphanRecording(Recording):
    channel = models.ForeignKey('EpiphanChannel', null=True)


@signal_connect
class RecordingAsset(TimeStampedModel):
    recording = models.ForeignKey(
        'Recording',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=128
    )
    data = models.FileField(
        upload_to=Uuid4Upload
    )
    mimetype = models.TextField()
    preview = ProcessedImageField(
        upload_to=Uuid4Upload,
        processors=[
            ResizeToFill(500, 50)
        ],
        format='JPEG',
        options={
            'quality': 60
        },
        null=True,
        blank=True
    )

    class Meta:
        ordering = (
            '-created',
        )
        permissions = (
            ('view_recordingasset', _('View Recording Asset')),
        )

    def __str__(self):
        return self.name

    def pre_delete(self, *args, **kwargs):
        self.data.delete(False)
        self.preview.delete(False)


class Export(TimeStampedModel, PolymorphicModel):
    recording = models.ForeignKey(
        'Recording',
        on_delete=models.CASCADE
    )


@signal_connect
class SideBySideExport(Export):
    data = models.FileField(
        upload_to=Uuid4Upload
    )

    class Meta:
        verbose_name = 'Side-by-Side'

    def process(self, notify):
        streams = self.recording.info['streams']
        vis = [s for s in streams if s['codec_type'] == 'video']
        height = max([v['coded_height'] for v in vis])
        videos = []
        for i, v in enumerate(vis):
            if v['coded_height'] < height:
                filt = 'pad=height={}'.format(height)
            else:
                filt = 'null'
            videos.append(
                (
                    '[i:{}]{}[v{}]'.format(v['id'], filt, i),
                    '[v{}]'.format(i),
                )
            )
        aus = [s for s in streams if s['codec_type'] == 'audio']
        fc = '{vf};{v}hstack=inputs={vl}[v];{a}amerge[a]'.format(
            vf=';'.join([v[0] for v in videos]),
            v=''.join([v[1] for v in videos]),
            vl=len(videos),
            a=''.join(['[i:{}]'.format(a['id']) for a in aus])
        )
        with NamedTemporaryFile(suffix='.mp4') as output:
            args = [
                'ffmpeg',
                '-y',
                '-i',
                self.recording.data.path,
                '-filter_complex',
                fc,
                '-map',
                '[v]',
                '-map',
                '[a]',
                '-ac',
                '2',
                output.name
            ]
            ffmpeg = Process(*args)
            ffmpeg.handler(FFMPEGProgressHandler(partial(notify, 'Stitching')))
            ffmpeg.run()
            self.data.save(output.name, File(output.file))

    def pre_delete(self, *args, **kwargs):
        self.data.delete(False)


@signal_connect
class ZipStreamExport(Export):
    data = models.FileField(
        upload_to=Uuid4Upload
    )

    class Meta:
        verbose_name = 'Zip-Stream'

    def process(self, notify):
        if 'streams' not in self.recording.info:
            from .tasks import ProcessRecordingTask
            ProcessRecordingTask().run(self.pk)
        mapping = {
            'h264': 'm4v',
            'aac': 'm4a',
        }
        streams = []
        args = [
            'ffmpeg',
            '-y',
            '-i',
            self.recording.data.path,
        ]
        with TemporaryDirectory(prefix='recording') as path:
            for s in self.recording.info['streams']:
                f = mapping.get(s['codec_name'])
                name = os.path.join(
                    path,
                    '{s[codec_type]}-{s[id]}.{f}'.format(s=s, f=f)
                )
                args.extend([
                    '-map',
                    'i:{s[id]}'.format(s=s),
                    '-c',
                    'copy',
                    name,
                ])
                streams.append(name)
            ffmpeg = Process(*args)
            ffmpeg.handler(FFMPEGProgressHandler(partial(notify, 'Splitting')))
            ffmpeg.run()
            with NamedTemporaryFile(suffix='.zip') as output:
                with ZipFile(output, 'w') as arc:
                    for i, f in enumerate(streams):
                        notify('Zipping', i + 1, len(streams))
                        arc.write(f, os.path.basename(f))
                        os.remove(f)
                self.data.save(output.name, File(output.file))

    def pre_delete(self, *args, **kwargs):
        self.data.delete(False)


class Stream(models.Model):
    name = models.CharField(max_length=128)
    enabled = models.BooleanField(default=True)
    active = models.ForeignKey('Broadcast', null=True, related_name='+')


class Broadcast(models.Model):
    stream = models.ForeignKey('Stream')
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, editable=False)


@signal_connect
class Token(models.Model):
    stream = models.ForeignKey('Stream')
    value = models.CharField(max_length=22)

    def pre_save(self, *args, **kwargs):
        if not self.value:
            v = urlsafe_b64encode(uuid.uuid4().bytes).decode('ascii').rstrip('=')
            self.value = v


#class Series(models.Model):
#    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#    title = models.CharField(max_length=256)
#    subject = models.CharField(max_length=256, blank=True)
#    description = models.TextField(blank=True)
#    license = models.ForeignKey('base.License')
#    rights = models.TextField(blank=True)
#    organizers = models.TextField(blank=True)
#    contributors = models.TextField(blank=True)
#    publishers = models.TextField(blank=True)
#
#    tags = TaggableManager()


class Event(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=256)
    subject = models.CharField(max_length=256, blank=True)
    description = models.TextField(blank=True)
    license = models.ForeignKey('base.License')
    rights = models.TextField(blank=True)
    presenters = models.TextField(blank=True)
    contributors = models.TextField(blank=True)
    room = models.ForeignKey('geo.Room', null=True, blank=True)

    tags = TaggableManager()


@signal_connect
class EventMedia(TimeStampedModel, PolymorphicModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=256,
    )
    data = models.FileField(
        upload_to=Uuid4Upload
    )
    info = JSONField(null=True)

    def pre_save(self, *args, **kwargs):
        self.info = FFProbeProcess(
            '-show_format',
            '-show_streams',
            self.data.path
        ).run()

    def post_save(self, *args, **kwargs):
        delete_memoized(self.response)

    def pre_delete(self, *args, **kwargs):
        self.data.delete(False)

    @memoize(timeout=3600)
    def response(self):

        data = {
            'pk': self.pk,
            'name': self.name,
            'url': self.data.url,
            'created': self.created,
            'modified': self.modified,
        }
        if self.info:
            data['container'] = {
                'format': self.info['format']['format_long_name'],
                'duration': float(self.info['format']['duration']),
                'size': self.data.size,
            }
            data['streams'] = []
            for s in self.info['streams']:
                data['streams'].append(
                    {
                        'codec': s['codec_long_name'],
                        'type': s['codec_type'],
                        'height': s.get('height', None),
                        'width': s.get('width', None),
                        'profile': s.get('profile', None),
                        'pixel': s.get('pix_fmt', None),

                    }
                )
        return data

    def __repr__(self):
        return '{s.__class__.__name__}({s.pk})'.format(s=self)


class EventAudio(EventMedia):
    pass


@signal_connect
class EventVideo(EventMedia):
    preview = ProcessedImageField(
        upload_to=Uuid4Upload,
        format='JPEG',
        options={'quality': 60}
    )

    def pre_save(self, *args, **kwargs):
        super().pre_save(*args, **kwargs)
        skip = float(self.info['format']['duration']) * 0.1
        with NamedTemporaryFile(suffix='.jpg', delete=True) as output:
            Process(
                'ffmpeg',
                '-y',
                '-ss',
                '{0:.2f}'.format(skip),
                '-i',
                self.data.path,
                '-vf',
                'thumbnail',
                '-frames:v',
                '1',
                output.name
            ).run()
            logger.info('Thumbnail: {}'.format(output.name))
            self.preview.save('preview.jpg', File(output.file), False)

    def response(self):
        data = super().response()
        data['preview'] = self.preview.url
        return data


class Publish(PolymorphicModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    event = models.ForeignKey(
        'Event',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )


class PublishMedia(PolymorphicModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    eventmedia = models.ForeignKey(
        'EventMedia',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )


class PublishMediaScene(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    media = models.ForeignKey(
        'PublishMedia',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    timestamp = models.PositiveIntegerField()
    image = ProcessedImageField(
        upload_to=Uuid4Upload,
        format='JPEG',
        options={'quality': 60}
    )
    words = ArrayField(
        models.CharField(max_length=512, blank=True),
        default=list
    )

    def pre_delete(self, *args, **kwargs):
        self.image.delete(False)


class DASHPublish(Publish):
    presenter = models.ForeignKey(
        'DASHVideo',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL
    )
    slides = models.ForeignKey(
        'DASHVideo',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL
    )
    audio = models.ForeignKey(
        'DASHAudio',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL
    )

    class Meta:
        permissions = (
            ('view_dash', _('View DASH')),
        )


class DASHIngest(models.Model):
    path = models.TextField()

    class Meta:
        abstract = True

    def ingest(self, path):
        p = Path(path)
        if not p.is_dir():
            logger.warn('Ingest failed because of missing directory: {}'.format(path))
            return
        mpd = p.joinpath('dash.mpd')
        with mpd.open() as f:
            tree = etree.parse(f)
        files = tree.xpath(
            '//m:Initialization/@sourceURL|//m:SegmentURL/@media',
            namespaces={
                'm': 'urn:mpeg:dash:schema:mpd:2011'
            }
        )
        if not files:
            logger.warn('No files found while ingesting: {}'.format(mpd))
            return
        if self.path:
            t = Path(self.path)
            if t.is_dir():
                for f in t.glob('*'):
                    f.unlink()
            else:
                t.mkdir(parents=True)
        else:
            base = Path(settings.OUTPOST.get('private_store'))
            c = Path(self.__module__, self._meta.object_name)
            u = urlsafe_b64encode(uuid4().bytes).decode('ascii').rstrip('=')
            t = base.joinpath(c).joinpath(u)
            t.mkdir(parents=True)
            self.path = str(t)
        target = Path(self.path)
        for f in map(lambda x: p.joinpath(x), files):
            f.rename(target.joinpath(f.name))
        mpd.rename(target.joinpath(mpd.name))

    def pre_delete(self, *args, **kwargs):
        shutil.rmtree(self.path)


class DASHVideo(PublishMedia):
    preview = ProcessedImageField(
        upload_to=Uuid4Upload,
        format='JPEG',
        options={'quality': 60}
    )

    class Meta:
        permissions = (
            ('view_dash_video', _('View DASH Video')),
        )


@signal_connect
class DASHVideoVariant(DASHIngest, models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    video = models.ForeignKey(
        'DASHVideo',
        on_delete=models.CASCADE
    )
    height = models.PositiveIntegerField()

    def pre_delete(self, *args, **kwargs):
        super().pre_delete(*args, **kwargs)


@signal_connect
class DASHAudio(DASHIngest, PublishMedia):

    class Meta:
        permissions = (
            ('view_dash_audio', _('View DASH Audio')),
        )

    def pre_delete(self, *args, **kwargs):
        super().pre_delete(*args, **kwargs)
