from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUsersApiTest(TestCase):
    """Test the users API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        """Test creating user with valid payload"""
        payload = {
            'email': 'kane@kane.com',
            'password': 'wordpass',
            'name': 'test user'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a duplicate user"""
        payload = {
            'email': 'kane@kane.com',
            'password': 'wordpass',
            'name': 'test user'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_password_length(self):
        """that that a password is more than 5 chars"""
        payload = {'email': 'me@memail.com', 'password': 'hi'}

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()
        
        self.assertFalse(user_exists)

