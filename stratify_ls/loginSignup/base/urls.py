from django.urls import path
from . import views #import views file
# from django.contrib.auth import views as auth_views

urlpatterns =[
    path('', views.Home, name='home'),
    path('register/', views.RegisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),

    #password
    path('forgot-password/', views.ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', views.ResetPassword, name='reset-password'),

    #view profile
    path('profile/<str:name>/', views.view_profile, name='view_profile'),

    path('my-activities/', views.MyActivities, name='my_activities'),
    path('messages/', views.Messages, name='messages'),
]
