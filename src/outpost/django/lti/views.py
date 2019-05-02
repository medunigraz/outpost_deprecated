from django.conf import settings
from django.contrib.auth import (
    get_user_model,
    login,
)
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect,
)
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import translation
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from lti import ToolConfig
from lti.contrib.django import DjangoToolProvider

from . import utils
from .models import (
    Consumer,
    GroupRole,
    Resource,
)


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
            return HttpResponseForbidden()

        try:
            consumer = Consumer.objects.get(
                key=tool_provider.consumer_key,
                enabled=True
            )
        except Consumer.DoesNotExist:
            return HttpResponseForbidden()

        params = tool_provider.to_params()
        username = params.get('ext_user_username')
        user = get_user_model().objects.get(username=username)
        login(
            request,
            user,
            backend='django.contrib.auth.backends.ModelBackend'
        )
        #import pudb; pu.db
        language = params.get(
            'launch_presentation_locale',
            settings.LANGUAGE_CODE
        )
        with translation.override(language):
            try:
                resource = Resource.objects.get(
                    consumer=consumer,
                    resource=params.get('resource_link_id')
                )
                return resource.render(
                    request,
                    consumer,
                    user,
                    tool_provider
                )
            except Resource.DoesNotExist:
                roles = params.get('roles')
                grs = GroupRole.objects.filter(role__in=roles)
                groups = user.groups.all()
                for gr in grs:
                    if gr.group not in groups:
                        user.groups.add(gr.group)
                if not user.has_perm('lti.add_resource'):
                    return HttpResponseForbidden()
                return TemplateResponse(
                    request,
                    'lti/index.html',
                    {
                        'consumer': consumer,
                        'user': user,
                        'tool_provider': tool_provider,
                        'resource_classes': Resource.__subclasses__()
                    }
                )
