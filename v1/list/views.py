#!/usr/bin/env python
# encoding: utf-8

from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import GroceryList, GroceryItem
from .serializers import GroceryListSerializer, \
    GroceryItemSerializer, BulkGroceryItemSerializer
from .permissions import IsListOwner, IsItemOwner


class GroceryListViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    lookup_field = 'slug'
    serializer_class = GroceryListSerializer
    permission_classes = (IsListOwner,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ('pub_date',)
    ordering = ('pub_date',)

    def get_queryset(self):
        user = self.request.user
        if user and not user.is_anonymous:
            return GroceryList.objects.filter(
                Q(author=user) | Q(groceryshared__shared_to=user)
            )
        return GroceryList.objects.none()


class GroceryItemViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Allows filtering by GroceryList `list={list_id}`
    """
    serializer_class = GroceryItemSerializer
    permission_classes = (IsItemOwner,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ('list',)
    ordering_fields = ('list_id', 'order', 'pk')
    ordering = ('list_id', 'order', 'pk')

    def get_queryset(self):
        user = self.request.user
        if user and not user.is_anonymous:
            return GroceryItem.objects.filter(
                Q(list__author=user) | Q(list__groceryshared__shared_to=user)
            )
        return GroceryItem.objects.none()


class BulkGroceryItemViewSet(ListBulkCreateUpdateDestroyAPIView):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions in bulk.
    See: https://github.com/miki725/django-rest-framework-bulk
    """
    serializer_class = BulkGroceryItemSerializer
    permission_classes = (IsItemOwner,)

    def get_queryset(self):
        user = self.request.user
        if user and not user.is_anonymous:
            return GroceryItem.objects.filter(
                Q(list__author=user) | Q(list__groceryshared__shared_to=user)
            ).order_by('list_id', 'order', 'pk')
        return GroceryItem.objects.none()

    def bulk_destroy(self, request, *args, **kwargs):
        qs = self.get_queryset()

        filtered = qs.filter(id__in=self.request.data)
        if not self.allow_bulk_destroy(qs, filtered):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        self.perform_bulk_destroy(filtered)

        return Response(status=status.HTTP_204_NO_CONTENT)
