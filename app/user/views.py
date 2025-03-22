from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import generics, authentication, permissions

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    #        * Người dùng gửi Token kèm theo yêu cầu HTTP (trong phần tiêu đề - headers).
    #       * Hệ thống xác minh token này để đảm bảo rằng người dùng đã đăng nhập hợp lệ.
    authentication_classes = [authentication.TokenAuthentication]
    #Lớp quyền này (IsAuthenticated) đảm bảo rằng chỉ những người dùng đã xác thực mới có thể truy cập endpoint này.
    permission_classes = [permissions.IsAuthenticated]

    #>< get_queryset ta override hàm get_object() để trả về đối tượng người dùng hiện tại (self.request.user)
    def get_object(self):
        #khi mà view gọi đến để lấy user thì nó sẽ qua hàm này
        """Retrieve and return the authenticated user."""
        print(f'GET Object: {self.request.user}')
        return self.request.user