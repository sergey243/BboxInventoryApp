from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes, action, api_view
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, status, generics


from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_auth.views import LoginView

from .serializers import (UserSerializer, LoginSerializer, CreateUserSerializer, ProfileSerializer)
from ..models import Profile
from utils.permissions import IsAuthenticated

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view()
def complete_view(request):
    return Response("Email account is activated")

class CustomLoginView(LoginView):
    def get_response(self):
        context = dict()
        orginal_response = super().get_response()
        context["profile"] = ProfileSerializer(self.request.user.profile).data
        context["username"] =  self.request.user.username

        orginal_response.data.update(context)
        return orginal_response

class ProfileViewset(RetrieveModelMixin,viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    from utils.permissions import IsAuthenticated
    def retrieve(self, request, pk=None):  
        queryset = Profile.objects.all()
        data = get_object_or_404(queryset, pk=pk)
        context = {'request': self.request}
        serializer = ProfileSerializer(data, context= context)
        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def save(self, request):
        queryset = Profile.objects.all()
        data = get_object_or_404(queryset, user_id=request.user)
        serializer = ProfileSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def load(self, request):
        if request.user.is_anonymous:
            raise Http404
        queryset = Profile.objects.all()
        data = get_object_or_404(queryset, user_id=request.user)
        context = {'request': self.request}
        serializer = ProfileSerializer(data, context= context)
        return Response(serializer.data)
    
