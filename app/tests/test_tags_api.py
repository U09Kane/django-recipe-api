from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag, Recipe
from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """Test publicly available tags api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is required for getting tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """test the private tags api"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'person@email.com',
            'sassword')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """test retrieving tags"""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """test that tags returned are only for authenticated user"""
        other_user = get_user_model().objects.create_user(
            'other@email.com',
            'wordthing')

        Tag.objects.create(user=other_user, name="Fruity")
        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """test creating a new tag"""
        payload = {'name': 'test'}
        self.client.post(TAGS_URL, payload)

        does_exist = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(does_exist)

    def test_create_invalid_tag(self):
        """test creating an invalid tag"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_tags_by_recipe(self):
        """test getting all tags associated with recipe"""
        tag1 = Tag.objects.create(user=self.user, name='Breakfast')
        tag2 = Tag.objects.create(user=self.user, name='Dinner')

        recipe = Recipe.objects.create(
            title='English Muffin',
            time_minutes=20,
            price=5.00,
            user=self.user)

        recipe.tags.add(tag1)
        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)
        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieved_tags_unique(self):
        """test that filtered tags are unique"""
        tag = Tag.objects.create(user=self.user, name='Breakfast')
        Tag.objects.create(user=self.user, name='Dinner')

        recipe1 = Recipe.objects.create(
            title='Pancakes',
            time_minutes=5,
            price=5.00,
            user=self.user)
        recipe2 = Recipe.objects.create(
            title='Porridge',
            time_minutes=3,
            price=2.00,
            user=self.user)

        recipe1.tags.add(tag)
        recipe2.tags.add(tag)
        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
