from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import (
    TemplateView,
    View,
)

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


class Template404View(TemplateView):
    template_name = 'outpost/404.html'


class Template500View(TemplateView):
    template_name = 'outpost/500.html'
