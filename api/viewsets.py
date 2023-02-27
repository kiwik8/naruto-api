from rest_framework import viewsets
from api.models import Character, Category
from rest_framework.response import Response
from api.serializers import *

class CharacterViewSet(viewsets.ReadOnlyModelViewSet):

    def get_language(self, request, language):
        if language is not None:
            request.session['language'] = language
            request.session.save()
        else:
            language = request.session.get('language', None)
        self.language = language
        return language

    def get_queryset(self):
        language = self.language
        if language == 'en':
            queryset = Character.objects.filter(fr_name=None)
        elif language == 'fr':
            queryset = Character.objects.filter(en_name=None)
        character_id = self.request.GET.get('id')
        if character_id is not None:
            queryset = queryset.filter(id=character_id)
        return queryset


    def get_serializer_class(self):
        serializer = CharacterListSerializer
        detail = CharacterDetailSerializer

        if self.action == 'retrieve':
            return detail
        return serializer

    
    def list(self, request, *args, **kwargs):
        language = kwargs.get('language', None)
        language = self.get_language(request, language)
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=queryset, many=True, language=language)
        serializer.is_valid(raise_exception=False)
        response = Response(serializer.data)
        return response


    def retrieve(self, request, pk=None, *args, **kwargs):
        language = kwargs.get('language', None)
        language = self.get_language(request, language)
        queryset = Character.objects.get(pk=pk)
        serializer = CharacterDetailSerializer(queryset, language=language)
        response = Response(serializer.data)
        return response




class CategoryViewSet(viewsets.ReadOnlyModelViewSet):


    def get_queryset(self):
        queryset = Category.objects.all()
        category_id = self.request.GET.get('id')
        if category_id is not None:
            queryset = queryset.filter(id=category_id)
        return queryset


    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return CategoryListSerializer
