#!/usr/bin/env python
# encoding: utf-8

from django.db import models
from django.utils.translation import gettext_lazy as _

from v1.recipe.models import Recipe


class IngredientGroup(models.Model):
    """
    Django Model to hold an Ingredient Groups.
    Ingredient Groups share a many to one relationship.
    Meaning each Recipe will have many Ingredient Groups.
    :title: = Title of the Ingredient Group (EX: Cheddar Biscuits)
    """
    title = models.CharField(_('title'), max_length=150, null=True, blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredient_groups')

    class Meta:
        unique_together = ('title', 'recipe')

    def __str__(self):
        return '%s' % self.title


class Ingredient(models.Model):
    """
    Django Model to hold an Ingredient.
    Ingredients share a many to one relationship.
    Meaning each Ingredient Group will have many Ingredients.
    :title: = Title of the Ingredient (EX: Flour)
    :numerator: = Numerator of the quantity expressed as a fraction
    :denominator: = Denominator of the quantity expressed as a fraction
    :measurement: = Measurement of the Ingredient (EX: Liters, Cups, Grams, tablespoons)
    :quantity: = Amount of the Ingredient Needed (EX: 200, 15, 2)
    """
    title = models.CharField(_('title'), max_length=250)
    numerator = models.FloatField(_('numerator'), default=0)
    denominator = models.FloatField(_('denominator'), default=1)
    measurement = models.CharField(_('measurement'), max_length=200, blank=True, null=True)
    ingredient_group = models.ForeignKey(IngredientGroup, on_delete=models.CASCADE, related_name='ingredients', null=True)

    def __str__(self):
        return '%s' % self.title
