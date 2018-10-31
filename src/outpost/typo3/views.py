import io
import logging

import requests
from django.http import (
    HttpResponse,
    HttpResponseNotFound,
)
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import View
from PIL import Image

from . import models

logger = logging.getLogger(__name__)


@method_decorator(cache_page(3600), name='dispatch')
class MediaView(View):

    def get(self, request, pk, width=None):
        media = get_object_or_404(models.Media, pk=pk)
        try:
            req = requests.get(media.url)
            with Image.open(io.BytesIO(req.content)) as img:
                fmt = img.format
                response = HttpResponse()
                if width:
                    width = int(width)
                    if img.width > width:
                        height = int(img.height * (width / float(img.width)))
                        img = img.resize((width, height), Image.ANTIALIAS)
                img.save(response, format=fmt)
                response['Content-Type'] = Image.MIME[fmt]
                response['Cache-Control'] = 'private,max-age=604800'
                return response
        except Exception as e:
            logger.warn(f'Failed to load image blob: {e}')
        return HttpResponseNotFound()
