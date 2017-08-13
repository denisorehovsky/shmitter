from django.conf.urls import url
from django.contrib.auth import get_user_model

from djoser import views as djoser_views

from .views import obtain_jwt_token

User = get_user_model()

urlpatterns = [
    url(
        r'^auth/token/obtain/$',
        obtain_jwt_token,
        name='obtain_token'
    ),
    url(
        r'^auth/register/$',
        djoser_views.RegistrationView.as_view(),
        name='register'
    ),
    url(
        r'^auth/activate/$',
        djoser_views.ActivationView.as_view(),
        name='activate'
    ),
    url(
        r'^auth/password/$',
        djoser_views.SetPasswordView.as_view(),
        name='set_password'
    ),
    url(
        r'^auth/password/reset/$',
        djoser_views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    url(
        r'^auth/password/reset/confirm/$',
        djoser_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
]
