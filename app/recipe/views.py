from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import Recipe
from recipe import serializers
from user.authentication import CustomJWTAuthentication


class RecipeViewSet(viewsets.ModelViewSet):  # When you need a complete set of CRUD operations for a resource
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeSerializer

    # represent object that is available for the Viewset,  points to all Recipe objects in the database.
    queryset = Recipe.objects.all()
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]  # chi doi tuong dang nhap moi xem duoc

    def get_queryset(self):  # get_queryset() trả về danh sách các đối tượng
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def create(self, request, *args, **kwargs):
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save(owner=request.user)

        request_info = {
            'status':status.HTTP_201_CREATED,
            'method': request.method,
            'path': request.path,
            'data': request.data,
        }
        return Response({**request_info},status=status.HTTP_201_CREATED)
