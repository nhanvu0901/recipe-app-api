from rest_framework import serializers

from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    # serializers.ModelSerializer provides a shortcut that automatically creates fields based on the model
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link','description']
        read_only_fields = ['id']

    def create(self, validated_data):
        print(validated_data)
        user = validated_data['owner']
        Recipe.objects.create(
            title=validated_data['title'],
            user=user,
            description=validated_data['description'],
            time_minutes=validated_data['time_minutes'],
            price=validated_data['price'],
        )
        del validated_data['owner']
        return validated_data


