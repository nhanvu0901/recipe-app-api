# Chuyển dữ liệu từ cơ sở dữ liệu (như các đối tượng Django model) thành JSON hoặc các định dạng khác mà API có thể trả về cho client.å
# cầu nối giữa model (dữ liệu trong database) và API
from datetime import timedelta
from django.utils import timezone
#database  ----- serializer ----- view ------- api call

from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import CustomToken


#DRF generates the fields automatically based on the model’s fields
# Structured around the Meta class, which links it to a model.
# Includes built-in create() and update() methods for model instances (which you can override)
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    # instance là biễn cũ ,
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance,validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


#Serializer
#Minimal structure: Just fields and optional methods like validate().
#No Meta class because it doesn’t need model metadata.
#Use when you’re working with non-model data or custom structures (e.g., login forms, API payloads not tied to a single model).
class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password,
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            # cách phổ biến để raise error , view sẽ chuyển thành 400 bad request
            raise serializers.ValidationError(msg, code='authorization')
        print(f"user: {user.password}")
        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Calculate expiration time based on ACCESS_TOKEN_LIFETIME
        expiration_time = timezone.now() + timedelta(minutes=60)  # Match SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        CustomToken.objects.create(
            user=user,
            access_token=access_token,
            refresh_token=refresh_token,
            tokenExpiredTime=expiration_time
        )
        return access_token, refresh_token, expiration_time