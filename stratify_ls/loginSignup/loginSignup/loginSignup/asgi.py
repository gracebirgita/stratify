"""
ASGI config for loginSignup project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# application = get_asgi_application()

# chat
# real-time communication

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
# from chat.routing import websocket_urlpatterns

# import base.routing
# application = ProtocolTypeRouter({
#     'http': get_asgi_application(),
#     # 'websocket' : AuthMiddlewareStack(
#     #     URLRouter(
#     #         # websocket_urlpatterns
#     #         chat.routing.websocket_urlpatterns
#     #     )
#     # ),
# })

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loginSignup.settings')

import chat.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
            # base.routing.websocket_urlpatterns
        )
    ),
})