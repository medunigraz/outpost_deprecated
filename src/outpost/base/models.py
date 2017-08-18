from django.db import models
from PIL import (
    Image,
    ImageColor,
    ImageOps,
)

from .utils import Uuid4Upload


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
