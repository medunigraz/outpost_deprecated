from . import api

v1 = [
    (
        r'networktoken/token',
        api.TokenViewSet,
        'networktoken-token'
    ),
]
