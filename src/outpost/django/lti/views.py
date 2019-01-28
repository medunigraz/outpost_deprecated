from django.contrib.auth import get_user_model
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
)
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from lti import ToolConfig
from lti.contrib.django import DjangoToolProvider

from . import utils


@method_decorator(csrf_exempt, name='dispatch')
class LTIView(View):

    def get(self, request, *args, **kwargs):
        app_title = 'My App'
        app_description = 'An example LTI App'
        launch_url = request.build_absolute_uri(reverse('lti:index'))

        extensions = {}

        lti_tool_config = ToolConfig(
            title=app_title,
            launch_url=launch_url,
            secure_launch_url=launch_url,
            extensions=extensions,
            description=app_description
        )

        lti_tool_config.icon = 'http://www.example.com/icon.png'

        return HttpResponse(lti_tool_config.to_xml(), content_type='text/xml')

    def post(self, request):
        tool_provider = DjangoToolProvider.from_django_request(request=request)
        validator = utils.OutpostRequestValidator()
        ok = tool_provider.is_valid_request(validator)
        if not ok:
            return HttpResponse()

        username = tool_provider.launch_params.get('ext_user_username')
        user = get_user_model().objects.get(username=username)
        return HttpResponse(f'LTI-Request erfolgreich, Benutzer {user} erkannt.')
