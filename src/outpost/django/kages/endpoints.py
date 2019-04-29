from . import api

v1 = [
    (
        r'kages/translate',
        api.TranslateViewSet,
        'kages-translate'
    ),
]
