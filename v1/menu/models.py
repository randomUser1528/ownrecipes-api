#!/usr/bin/env python
# encoding: utf-8

from django.db import models
from django.contrib.auth.models import User

from v1.recipe.models import Recipe


class MenuItem(models.Model):
    """
    Django Model to hold a Recipe that is related to a menu.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='menu_recipe')
    complete = models.BooleanField(default=False, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    complete_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.recipe.title
