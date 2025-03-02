from django.urls import path, include, re_path

urlpatterns = [
    path('accounts/', include('allauth.urls')),
]