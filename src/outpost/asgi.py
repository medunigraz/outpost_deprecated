import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'outpost.settings')
django.setup() # NOQA

from channels.auth import AuthMiddlewareStack
from channels.routing import (
    ProtocolTypeRouter,
    URLRouter,
)

from outpost.base.routing import websocket_urlpatterns


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
