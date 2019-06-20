from rest_framework.serializers import ModelSerializer
from core.models import Tag, Ingredient


class TagSerializer(ModelSerializer):
    """Serializer for <Tag> object"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id', )


class IngredientSerializer(ModelSerializer):
    """Serializer for <Ingredient>"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only = ('id',)
