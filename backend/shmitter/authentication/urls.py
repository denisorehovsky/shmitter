from django.conf.urls import url
from django.contrib.auth import get_user_model

from djoser import views as djoser_views

from .views import obtain_jwt_token

User = get_user_model()

urlpatterns = [
    url(r'^login/$', obtain_jwt_token, name='login'),
    url(r'^register/$', djoser_views.RegistrationView.as_view(), name='register'),
    url(r'^activate/$', djoser_views.ActivationView.as_view(), name='activate'),
    url(r'^password/$', djoser_views.SetPasswordView.as_view(), name='set_password'),
    url(r'^password/reset/$', djoser_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password/reset/confirm/$', djoser_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
