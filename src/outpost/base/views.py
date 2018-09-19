from celery.result import AsyncResult
from django.http import (
    HttpResponse,
    JsonResponse,
)
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    TemplateView,
    View,
)
from wand.image import Image

from . import models


class IndexView(TemplateView):
    template_name = 'outpost/index.html'


class ColorizedIconView(View):

    def get(self, request, pk, color):
        icon = get_object_or_404(models.Icon, pk=pk)
        response = HttpResponse(content_type='image/png')
        image = icon.colorize(color)
        image.save(response, 'PNG')
        return response


class TaskView(View):

    def get(self, request, task):
        result = AsyncResult(task)
        return JsonResponse(
            {
                'state': result.state,
                'info': result.info
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class ImageConvertView(TemplateView):
    template_name = 'outpost/image-convert.html'

    def post(self, request, format):
        if not format:
            format = 'PDF'
        response = HttpResponse()
        with Image(file=request) as img:
            img.format = format.upper()
            img.save(response)
            response['Content-Type'] = img.mimetype
        return response


class ErrorView(TemplateView):

    def get_template_names(self):
        code = self.kwargs.get('code', 500)
        return [f'outpost/error/{code}.html', 'outpost/error.html']
