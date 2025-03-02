from django.urls import path, include, re_path
from allauth.account.views import ConfirmEmailView, TemplateView, confirm_email
from .views import  ProfileViewset, FacebookLogin, GoogleLogin, null_view, complete_view, CustomLoginView


urlpatterns = [
    path('', include('rest_auth.urls')),
    path('accounts/', include('allauth.urls')),
    re_path(r'custom/login/', CustomLoginView.as_view(), name='my_custom_login')
]