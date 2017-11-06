from rest_framework.metadata import SimpleMetadata
from django.contrib.auth.models import Permission


class ExtendedMetadata(SimpleMetadata):

    def determine_metadata(self, request, view):
        metadata = super().determine_metadata(request, view)
        if hasattr(view, 'get_queryset'):
            model = view.get_queryset().model
            permissions = Permission.objects.filter(
                content_type__app_label=model._meta.app_label,
                content_type__model=model._meta.model_name
            )
            #import pudb; pu.db
            metadata.update({
                'permissions': {p.codename: p.name for p in permissions}
            })


        return metadata
