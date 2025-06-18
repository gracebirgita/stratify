from django.urls import re_path
from django.urls import path
from . import consumers

websocket_urlpatterns =[
    # path('chat/', consumers.ChatConsumer.as_asgi()),

    # re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
     re_path(r'ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
]



# from django.urls import path
# from . import consumers
# from .views import chat_view

