from rest_framework import generics, authentication, permissions, status
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token  # Add this import
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import CustomToken
from user.authentication import CustomJWTAuthentication
from user.serializers import UserSerializer, AuthTokenSerializer

from datetime import timedelta


class CreateUserView(generics.CreateAPIView):  # Dùng để tạo user POST
    """Create a new user in the system."""
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        # Validate and create the user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # This calls UserSerializer.create()

        # Generate a token for the new user
        token, created = Token.objects.get_or_create(user=user)

        # Prepare response with user data and token
        data = serializer.data
        data['token'] = token.key
        return Response(data, status=201)  # 201 = Created


# Dùng để Retrieve or update the authenticated user GET /PUT /PATCH
class ManageUserView(generics.RetrieveAPIView):  # When you need specific, limited operations on a resource
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    #        * Người dùng gửi Token kèm theo yêu cầu HTTP (trong phần tiêu đề - headers).
    #       * Hệ thống xác minh token này để đảm bảo rằng người dùng đã đăng nhập hợp lệ.
    authentication_classes = [CustomJWTAuthentication] # JWTAuthentication /
    # Lớp quyền này (IsAuthenticated) đảm bảo rằng chỉ những người dùng đã xác thực mới có thể truy cập endpoint này.
    permission_classes = [permissions.IsAuthenticated]

    # def initial(self, request, *args, **kwargs):
    #     # This runs before get_object() or any HTTP method handler
    #     print(f"Request headers: {request.headers}")
    #     print(f"Raw token from header: {request.headers.get('Authorization')}")
    #     print(f"Authenticated user: {request.user}")
    #     print(f"Is authenticated? {request.user.is_authenticated}")
    #     return super().initial(request, *args, **kwargs)

    # >< get_queryset ta override hàm get_object() để trả về đối tượng người dùng hiện tại (self.request.user)
    def get_object(self):
        # khi mà view gọi đến để lấy user thì nó sẽ qua hàm này
        """Retrieve and return the authenticated user."""
        print(f'GET Object: {self.request.user}')
        return self.request.user


class CreateTokenView(APIView):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    def get(self, request, format=None):
        return Response({"message": "Success"}, status=200)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)  # trigger the validate method of AuthTokenSerializer

        access_token, refresh_token, expiration_time = serializer.save()# call the create method

        request_info = {
            'method': request.method,
            'path': request.path,
            'data': request.data,
        }
        return Response({'access': access_token,
                         'refresh': refresh_token, 'tokenExpiredTime': expiration_time.isoformat(),
                         **request_info}, status=status.HTTP_201_CREATED)
