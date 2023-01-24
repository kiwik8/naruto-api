from rest_framework import viewsets
from api.models import Character, Category
from api.serializers import *

class CharacterViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CharacterListSerializer
    detail_serializer_class = CharacterDetailSerializer

    def get_queryset(self):
        queryset = Character.objects.all()
        character_id = self.request.GET.get('id')
        if character_id is not None:
            queryset = queryset.filter(id=character_id)
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return self.serializer_class


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        category_id = self.request.GET.get('id')
        if category_id is not None:
            queryset = queryset.filter(id=category_id)
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return self.serializer_class
