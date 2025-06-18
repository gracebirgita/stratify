from django.urls import path, include # include -> path to other app
from . import views #import views file
# from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    path('home/', views.Home, name='home'),
    path('',views.landingPage, name='landingPage'),
    
    
    path('login/', views.loginRegisterView, name='login'),
    path('register/', views.loginRegisterView, name='register'),
    
    # path('register/', views.RegisterView, name='register'),
    # path('login/', views.LoginView, name='login'),
    
    path('logout/', views.LogoutView, name='logout'),

    #password
    path('forgot-password/', views.ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', views.ResetPassword, name='reset-password'),

    #view profile
    path('profile/<str:name>/', views.view_profile, name='view_profile'),
    path('profile/<str:name>/edit/', views.edit_profile, name='edit_profile'),
    path('activity/add/', views.add_activity, name='add_activity'),
    #view_profile(invest)
    path('invest/<str:company_name>/', views.invest, name='invest'),
    path('my-activities/', views.MyActivities, name='my_activities')

    # path('chat/<str:username>/', chatPage, name='chat'),
    # path('messages/', views.Messages, name='messages'),
    path('chat/', include('chat.urls')), 
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
