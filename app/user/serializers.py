# Chuyển dữ liệu từ cơ sở dữ liệu (như các đối tượng Django model) thành JSON hoặc các định dạng khác mà API có thể trả về cho client.å
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers


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
