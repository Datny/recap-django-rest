from decimal import Decimal

from core import models
from django.contrib.auth import get_user_model
from django.test import TestCase


def create_user(email='user@example.com', password='testpass123'):
    """Create and return new user"""
    return get_user_model().objects.create_user(email=email, password=password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password="some_password"
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raise_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='', password='pass123')

    def test_create_super_user(self):
        email = "test@example.com"
        password = 'testpw123'
        user = get_user_model().objects.create_superuser(email=email,
                                                         password=password)

        self.assertEqual(user.is_superuser, True)

    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)
