from django import forms
from django.forms.models import modelform_factory
from django.urls import reverse_lazy as reverse
from oauth2_provider.views import application
from oauth2_provider.models import get_application_model


class ApplicationModelFormMixin(object):

    def get_form_class(self):
        return modelform_factory(
            get_application_model(),
            fields=(
                'name',
                'description',
                'logo',
                'website',
                'privacy',
                'agree',
                'client_type',
                'authorization_grant_type',
                'redirect_uris',
            ),
            exclude=(
                'user',
                'client_id',
                'client_secret',
                'skip_authorization',
            ),
            widgets={
                'website': forms.TextInput,
                'privacy': forms.TextInput,
            }
        )


class ApplicationListView(application.ApplicationList):
    pass


class ApplicationDetailView(application.ApplicationDetail):
    pass


class ApplicationCreateView(ApplicationModelFormMixin, application.ApplicationRegistration):
    template = None
    success_url = reverse('oauth2:list')


class ApplicationEditView(ApplicationModelFormMixin, application.ApplicationUpdate):
    template = None
    success_url = reverse('oauth2:list')


class ApplicationDeleteView(application.ApplicationDelete):
    success_url = reverse('oauth2:list')
