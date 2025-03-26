from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Products."""
    # serializers.ModelSerializer provides a shortcut that automatically creates fields based on the model
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock','user']
        read_only_fields = ['id']