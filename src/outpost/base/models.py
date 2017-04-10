from PIL import (
    Image,
    ImageOps,
    ImageColor,
)

from django.db import models

from .utils import Uuid4Upload


class Icon(models.Model):
    name = models.CharField(
        max_length=128
    )
    image = models.FileField(
        upload_to=Uuid4Upload
    )

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
