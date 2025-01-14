#!/usr/bin/env python
# encoding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from v1.recipe.models import Recipe


class Rating(models.Model):
    """
    Django Model to hold a Rating of a recipe.
    Ratings share a many to one relationship.
    Meaning each Recipe will have many Ratings.
    :author: = User that created the comment
    :recipe: = The recipe the comment is related to
    :comment: = A comment on the recipe
    :rating: = A rating 1-5
    :pub_date: = When the rating was created
    :update_date: = When the rating was updated
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    comment = models.CharField(_('comment'), max_length=1000)
    rating = models.IntegerField(_('rating'), default=0)
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s - %s' % (self.rating, self.comment)
