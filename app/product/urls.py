from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from .views import ProductViewSet

#automatically create router because it is viewset
router = DefaultRouter()
router.register('product', ProductViewSet)

app_name = 'product'

urlpatterns = [
    path('', include(router.urls)),
]