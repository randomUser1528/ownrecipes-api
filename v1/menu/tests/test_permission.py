#!/usr/bin/env python
# encoding: utf-8

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from v1.menu.permissions import IsMenuItemOwner
from v1.menu.models import MenuItem


class PermissionTest(TestCase):
    fixtures = [
        'test/users.json',
        'course_data.json',
        'cuisine_data.json',
        'recipe_data.json',
        'ing_data.json'
    ]

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        # Create a staff user.
        self.staff = User.objects.create_user(
            username='staff', email='staff@gmail.com', password='top_secret', is_superuser=True
        )
        self.user = User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret'
        )
        self.item = MenuItem.objects.create(author=self.user, recipe_id=1)

    def test_is_item_owner_or_read_only(self):
        # Try and access something as an admin user.
        # Both get and post should have access.
        request = self.factory.get(f'/{settings.ADMIN_URL}')
        request.user = self.staff
        self.assertTrue(IsMenuItemOwner().has_object_permission(request, None, None))
        self.assertTrue(IsMenuItemOwner().has_object_permission(request, None, self.item))
        request = self.factory.post(f'/{settings.ADMIN_URL}')
        request.user = self.staff
        self.assertTrue(IsMenuItemOwner().has_object_permission(request, None, None))
        self.assertTrue(IsMenuItemOwner().has_object_permission(request, None, self.item))

        # Try and access something as an user who created th lists.
        # Both get and post should have access.
        request = self.factory.get(f'/{settings.ADMIN_URL}')
        request.user = self.user
        self.assertTrue(IsMenuItemOwner().has_object_permission(request, None, self.item))
        request = self.factory.post(f'/{settings.ADMIN_URL}')
        request.user = self.user
        self.assertTrue(IsMenuItemOwner().has_object_permission(request, None, self.item))

        # Try and access something as an anonymous user.
        # Both get and post should not have access.
        request = self.factory.get(f'/{settings.ADMIN_URL}')
        request.user = AnonymousUser()
        self.assertFalse(IsMenuItemOwner().has_object_permission(request, None, self.item))
        request = self.factory.post(f'/{settings.ADMIN_URL}')
        request.user = AnonymousUser()
        self.assertFalse(IsMenuItemOwner().has_object_permission(request, None, self.item))
