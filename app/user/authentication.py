from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import CustomToken


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        auth = super().authenticate(request)

        if auth is None:
            return None
        user, token = auth
        try:
            custom_token = CustomToken.objects.get(access_token=str(token))
            if custom_token.tokenExpiredTime and custom_token.tokenExpiredTime < timezone.now():
                raise AuthenticationFailed('Token has expired according to CustomToken')
            return custom_token.user, token
        except CustomToken.DoesNotExist:
            return user, token