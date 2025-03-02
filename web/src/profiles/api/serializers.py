from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_auth.registration.serializers import RegisterSerializer
from ..models import Profile

class CustomRegistrationSerializer(RegisterSerializer):

    def save(self, request):
        user = super(CustomRegistrationSerializer, self).save(request)
        user.is_active = False
        return user

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password','email',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        User = get_user_model()
        user = User.objects.create_user(validated_data['username'],
                                        None,
                                        validated_data['password'],
                                        validated_data['email'])
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model   = get_user_model()
        fields  = ('id','username','first_name','last_name','email')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to provide credentials")

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("first_name","last_name","birth_date","address","mobile","email",
            "picture","user","grade","branch")
        readread_only_fields =(
            "user",
        )