from . import api

v1 = [
    (
        r'structure/organization',
        api.OrganizationViewSet,
        'structure-organization'
    ),
    (
        r'structure/person',
        api.PersonViewSet,
        'structure-person'
    ),
]
