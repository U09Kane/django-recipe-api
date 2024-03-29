from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for <Tag> object"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id', )


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for <Ingredient>"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for <Recipe> object"""

    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all())

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = (
            'id',
            'title',
            'ingredients',
            'tags',
            'time_minutes',
            'price'
        )
        read_only = ('id', )


class RecipeDetailSerializer(RecipeSerializer):
    """Serialize a detail recipe"""
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for adding images to recipes"""

    class Meta:
        model = Recipe
        fields = ('id', 'image')
        read_only_fields = ('id',)
