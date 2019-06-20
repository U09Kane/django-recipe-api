from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Tag, Ingredient
from recipe import serializers


class TagViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """return objects for current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """create new tag"""
        serializer.save(user=self.request.user)


class IngredientViewSet(GenericViewSet, ListModelMixin):
    """Mange ingredients in database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        """return objects for current authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
