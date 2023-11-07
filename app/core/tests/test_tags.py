"""
Test for tags API
"""

from core.models import Tag
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from recipe.serializers import TagSerializer
from rest_framework import status
from rest_framework.test import APIClient

TAGS_URS = reverse('recipe:tag-list')


def create_user(email='user@example.com', password='testpass123'):
    """Create and return new user"""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicTagsApiTests(TestCase):
    """Test unauthenticated tags API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """auth is required to retrieve Tags"""
        res = self.client.get(TAGS_URS)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test authenticated tags API access"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(user=self.user, name="Vegan")
        Tag.objects.create(user=self.user, name="Dessert")

        res = self.client.get(TAGS_URS)

        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(serializer.data, res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_tags_limited_to_user(self):
        """Test list of tags is limited to authenitaced user"""

        user_2 = create_user(email='user2@example.com')
        Tag.objects.create(user=user_2, name='Fruity')

        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        res = self.client.get(TAGS_URS)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)
