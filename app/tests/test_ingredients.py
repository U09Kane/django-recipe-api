from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredient, Recipe
from recipe.serializers import IngredientSerializer


INGREDIENT_URL = reverse('recipe:ingredient-list')


class PublicIngredientApiTest(TestCase):
    """Test public ingredient apis"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is required to use api"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTest(TestCase):
    """Test that ingredients can be retrieved by authorized user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'password')

        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """test to retrieve a list of ingredients"""
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """test that ingredients are scoped to user"""
        other_user = get_user_model().objects.create_user(
            'other@email.com',
            'secondFiddle')

        Ingredient.objects.create(
            user=other_user,
            name='Chili Powder')

        ingredient = Ingredient.objects.create(
            user=self.user,
            name='Thyme')

        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """test creation of new ingredient"""
        payload = {'name': 'Onions'}
        self.client.post(INGREDIENT_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_ingredient_invalid(self):
        payload = {'name': ''}
        res = self.client.post(INGREDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_ingredients_by_recipe(self):
        """test getting tags that have been assigned a recipe"""
        ingredient1 = Ingredient.objects.create(
            user=self.user,
            name='Apples')
        ingredient2 = Ingredient.objects.create(
            user=self.user,
            name='Oranges')
        recipe = Recipe.objects.create(
            title='Apple Pie',
            time_minutes=30,
            price=10.00,
            user=self.user)

        recipe.ingredients.add(ingredient1)
        serializer1 = IngredientSerializer(ingredient1)
        serializer2 = IngredientSerializer(ingredient2)
        res = self.client.get(INGREDIENT_URL, {'assigned_only': 1})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_unique_ingredients(self):
        """test retrieving all unique ingredients"""
        ingredient = Ingredient.objects.create(name='Eggs', user=self.user)
        Ingredient.objects.create(name='Cheese', user=self.user)
        recipe1 = Recipe.objects.create(
            title='Eggs Bendict',
            time_minutes=15,
            price=4.00,
            user=self.user)
        recipe2 = Recipe.objects.create(
            title='Egg McMuffin',
            time_minutes=1,
            price=3.00,
            user=self.user)

        recipe1.ingredients.add(ingredient)
        recipe2.ingredients.add(ingredient)
        res = self.client.get(INGREDIENT_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
