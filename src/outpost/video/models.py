import re
import requests
import base64
from hashlib import sha256, md5
import json
import logging
import subprocess
import uuid
from base64 import urlsafe_b64encode, b64encode
from tempfile import NamedTemporaryFile
from uuid import uuid4
from purl import URL

import asyncssh
from django.db import models
from django.core.files import File
from django.contrib.postgres.fields import JSONField
from django_extensions.db.models import TimeStampedModel
from imagekit.models import ProcessedImageField
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
from ..base.utils import Uuid4Upload
from .utils import FFMPEGProcess

logger = logging.getLogger(__name__)


@signal_connect
class Server(models.Model):
    hostname = models.CharField(max_length=128, blank=True)
    port = models.PositiveIntegerField(default=2022)
    key = models.BinaryField(null=False)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = (
            ('hostname', 'port'),
        )

    @property
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

    def __str__(self):
        if self.hostname:
            return '{s.hostname}:{s.port}'.format(s=self)
        return '*:{s.port}'.format(s=self)


class Recorder(PolymorphicModel):
    name = models.CharField(max_length=128, blank=False, null=False)
    hostname = models.CharField(max_length=128, blank=False, null=False)
    active = models.BooleanField(default=True)
    room = models.ForeignKey(
        'geo.Room',
        null=True,
        blank=True
    )

    def __str__(self):
        return '{s.name} ({s.hostname})'.format(s=self)


@signal_connect
class Epiphan(Recorder):
    username = models.CharField(max_length=128, blank=False, null=False)
    password = models.CharField(max_length=128, blank=False, null=False)
    server = models.ForeignKey('Server', related_name='+')
    key = models.BinaryField(null=False)


    @property
    def fingerprint(self):
        if not self.key:
            return None
        k = asyncssh.import_private_key(self.key.tobytes())
        d = md5(k.get_ssh_public_key()).hexdigest()
        return ':'.join(a + b for a, b in zip(d[::2], d[1::2]))

    @property
    def private_key(self):
        return self.key.tobytes().decode('ascii')

    def post_init(self, *args, **kwargs):
        self.session = requests.Session()
        if self.username and self.password:
            self.session.auth = (self.username, self.password)
        self.url = URL(
            scheme='http',
            host=self.hostname,
            path='/admin/channelm1/'
        )

    def pre_save(self, *args, **kwargs):
        if self.key:
            return
        pk = asyncssh.generate_private_key('ssh-rsa', comment=self.name)
        # For compatibility with older SSH implementations
        self.key = pk.export_private_key('pkcs1-pem')
        self.save()

    @property
    def recording(self):
        url = self.url.add_path_segment('get_params.cgi').query_param('rec_enabled', '')
        try:
            r = self.session.get(url.as_string(), timeout=2)
        except requests.exceptions.ConnectionError:
            return False
        return re.match('^rec_enabled = on$', r.text) is not None


@signal_connect
class Recording(TimeStampedModel):
    recorder = models.ForeignKey('Recorder')
    data = models.FileField(
        upload_to=Uuid4Upload
    )
    info = JSONField()

    def pre_delete(self, *args, **kwargs):
        self.data.delete(False)


class Export(PolymorphicModel):
    recording = models.ForeignKey(
        'Recording',
    )


@signal_connect
class SideBySideExport(Export):
    data = models.FileField(
        upload_to=Uuid4Upload
    )

    class Meta:
        verbose_name = 'Side-by-Side'

    def process(self, notify):
        with NamedTemporaryFile(suffix='.mp4') as output:
            args = [
                '-i',
                self.recording.data.path,
                '-filter_complex',
                '[i:0x100][i:0x102]hstack=inputs=2[v];[i:0x101][i:0x103]amerge[a]',
                '-map',
                '[v]',
                '-map',
                '[a]',
                '-ac',
                '2',
                output.name
            ]
            FFMPEGProcess(args, notify)
            self.data.save(output.name, File(output.file))

    def pre_delete(self, *args, **kwargs):
        self.data.delete(False)

#class Publisher(PolymorphicModel):
#    name = models.CharField(max_length=128)
#    enabled = models.BooleanField(default=True)
#
#
#class YoutubePublisher(Publisher):
#    pass
#
#
#class OpencastPublisher(Publisher):
#    api = models.URLField()
#    username = models.CharField(max_length=128)
#    password = models.CharField(max_length=128)
#
#    def publish(self, rec):
#        u = URL(self.api).add_path_segment('events')
#        s = Session()
#        s.auth = (self.username, self.password)
#        fields = {
#            'acl': json.dumps(
#                [
#                    {
#                        'action': 'write',
#                        'role': 'ROLE_ADMIN',
#                    },
#                    {
#                        'action': 'read',
#                        'role': 'ROLE_USER',
#                    },
#                ]
#            ),
#            'metadata': json.dumps(
#                [
#                    {
#                        'flavor': 'dublincore/episode',
#                        'fields': [
#                            {
#                                'id': 'title',
#                                'value': 'Captivating title',
#                            },
#                            {
#                                'id': 'subjects',
#                                'value': ['John Clark', 'Thiago Melo Costa'],
#                            },
#                            {
#                                'id': 'description',
#                                'value': 'A great description',
#                            },
#                            {
#                                'id': 'startDate',
#                                'value': '2016-06-22',
#                            },
#                            {
#                                'id': 'startTime',
#                                'value': '13:30:00Z',
#                            },
#                        ]
#                    }
#                ]
#            ),
#            'processing': json.dumps(
#                {
#                    'workflow': 'ng-schedule-and-upload',
#                    'configuration': {
#                        'flagForCutting': 'false',
#                        'flagForReview': 'false',
#                        'publishToEngage': 'true',
#                        'publishToHarvesting': 'true',
#                        'straightToPublishing': 'true',
#                    },
#                }
#            ),
#        }
#        videos = {
#            'presenter': ('0x100', '0x101'),
#            'slides': ('0x102',),
#        }
#
#        args = ['ffmpeg', '-y', '-i', rec.data.path]
#        for video, streams in videos.items():
#            for stream in streams:
#                args.extend(['-map', 'i:{}'.format(stream)])
#            # Create temporary file for demux
#            tmp = NamedTemporaryFile(delete=False)
#            args.extend(['-c', 'copy', '-f', 'mp4', tmp.name])
#            fields[video] = (
#                video,
#                tmp,
#                'video/mp4'
#            )
#        logger.debug('Running: {}'.format(' '.join(args)))
#        proc = subprocess.run(args)
#        m = MultipartEncoder(fields=fields)
#        # Upload to server
#        event = s.post(u.as_string(), data=m)
#        if event.status_code == codes.ok:
#            uid = event.json().get('identifier')
#            logger.info('Published recording to {s} as {u}'.format(s=self, u=uid))
#        else:
#            logger.error('Publishing failed on {s}: {e}'.format(s=self, e=event.status_code))
#        # Delete all temporary files
#        for video in videos.keys():
#            fields[video][1].close()
#
#
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
            v = urlsafe_b64encode(uuid4().bytes).decode('ascii').rstrip('=')
            self.value = v
#
#
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
#
#
#class Event(models.Model):
#    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#    serie = models.ForeignKey('Series', null=True)
#    title = models.CharField(max_length=256)
#    subject = models.CharField(max_length=256, blank=True)
#    description = models.TextField(blank=True)
#    license = models.ForeignKey('base.License')
#    rights = models.TextField(blank=True)
#    presenters = models.TextField(blank=True)
#    contributors = models.TextField(blank=True)
#
#    tags = TaggableManager()
#
#
#class Media(PolymorphicModel):
#    event = models.ForeignKey('Event')
#    data = models.FileField(
#        upload_to=Uuid4Upload
#    )
#
#
#class VideoCategory(models.Model):
#    name = models.CharField(max_length=128)
#
#
#class Video(Media):
#    preview = ProcessedImageField(
#        upload_to=Uuid4Upload,
#        format='JPEG',
#        options={'quality': 60}
#    )
#    category = models.ForeignKey('VideoCategory')
#
#
#class Audio(Media):
#    pass
#
#
#class Subtitles(Media):
#    pass
#
#
#class Slides(Media):
#    pass
