#!/usr/bin/env python
# encoding: utf-8

from rest_framework import permissions, viewsets

from .models import Ingredient, IngredientGroup
from .serializers import IngredientSerializer, IngredientGroupSerializer
from v1.common.permissions import IsOwnerOrReadOnly


class IngredientGroupViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Ingredients.
    """
    queryset = IngredientGroup.objects.all()
    serializer_class = IngredientGroupSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    )
    filterset_fields = ('recipe',)
    ordering_fields = ('id',)


class IngredientViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Ingredients.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    )
    filterset_fields = ('ingredient_group', 'ingredient_group__recipe')
    ordering_fields = ('id',)
