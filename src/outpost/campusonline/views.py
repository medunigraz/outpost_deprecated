import logging

from django.http import (
    HttpResponse,
    HttpResponseNotFound,
)
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import View
from wand.exceptions import WandException
from wand.image import Image

from . import models

logger = logging.getLogger(__name__)


@method_decorator(cache_page(3600), name='dispatch')
class PrivateAvatarView(View):

    def get(self, request, hash):
        p = get_object_or_404(models.Person, hash=hash)
        try:
            with Image(blob=p.avatar_private.tobytes()) as img:
                response = HttpResponse()
                img.format = 'jpeg'
                img.save(file=response)
                response['Content-Type'] = img.mimetype
                response['Cache-Control'] = 'private,max-age=604800'
                return response
        except WandException as e:
            logger.warn(f'Failed to load image blob: {e}')
        return HttpResponseNotFound()
