from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from core.models import Tag, Ingredient
from recipe import serializers
from core.models import Recipe


class RecipeAttributeViewSet(GenericViewSet, ListModelMixin,
                             CreateModelMixin):
    "Viewset for reciple attributes e.g. tags & ingredients"
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """return objects for the current authenticated user"""
        return self.queryset.filter(
            user=self.request.user
        ).order_by('-name')

    def perform_create(self, serializer):
        """create new Attribute object"""
        serializer.save(user=self.request.user)


class TagViewSet(RecipeAttributeViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(RecipeAttributeViewSet):
    """Mange ingredients in database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(ModelViewSet):
    """Manage recipes within the database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """get recipes for authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """return serializer class"""
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer):
        """create a new recipe"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """upload image for a recipe"""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)
