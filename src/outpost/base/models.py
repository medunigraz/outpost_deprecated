import logging
import subprocess
from django.db import models
from PIL import (
    Image,
    ImageColor,
    ImageOps,
)

from .utils import Uuid4Upload

logger = logging.getLogger(__name__)


class NetworkedDeviceMixin(models.Model):
    hostname = models.CharField(max_length=128, blank=False, null=False)
    enabled = models.BooleanField(default=True)
    online = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def update(self):
        logger.debug('{s} starting ping: {s.online}'.format(s=self))
        proc = subprocess.run(
            [
                'ping',
                '-c1',
                '-w2',
                self.hostname
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL

        )
        online = (proc.returncode == 0)
        if self.online != online:
            self.online = online
            logger.debug('{s} online: {s.online}'.format(s=self))
            self.save()


class Icon(models.Model):
    name = models.CharField(
        max_length=128
    )
    image = models.FileField(
        upload_to=Uuid4Upload
    )

    def __str__(self):
        return self.name

    def colorize(self, color):
        image = Image.open(self.image.path)
        saturation = image.convert('L')
        result = ImageOps.colorize(
            saturation,
            ImageColor.getrgb('#{0}'.format(color)),
            (255, 255, 255)
        )
        result = result.convert('RGBA')
        result.putalpha(image.split()[3])
        return result


class License(models.Model):
    name = models.CharField(max_length=128)
    text = models.TextField()
