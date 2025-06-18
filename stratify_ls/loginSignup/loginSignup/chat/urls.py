from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns=[
    # path('chat/', include('chat.urls'))
    # path('admin/', admin.site.urls),
    # path('search-users/', views.search_users, name='search_users'),
    # path('get-messages/', views.get_messages, name='get_messages'),
    # path('', views.messages_page, name='messages'),
    # path('', views.chat_landing, name='chat_landing'),
    path('<str:room_name>/', views.messages_page, name='messages'),
]