from rest_framework import serializers
from api.models import Character, Category


class CharacterNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ('id', 'name')

class CategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CharacterListSerializer(serializers.ModelSerializer):

    categories = serializers.SerializerMethodField()

    class Meta:
        model = Character
        fields = ('id', 'name', 'description', 'image', 'categories')

    def get_categories(self, obj):
        return CategoryNameSerializer(obj.categories.all(), many=True).data

class CharacterDetailSerializer(serializers.ModelSerializer):

    categories = serializers.SerializerMethodField()

    class Meta:
        model = Character
        fields = ('id', 'name', 'description', 'image', 'categories', 'general_infos')

    def get_categories(self, obj):
        return CategoryNameSerializer(obj.categories.all(), many=True).data


class CategoryListSerializer(serializers.ModelSerializer):

    characters = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'characters')

    def get_characters(self, obj):
        return CharacterNameSerializer(obj.characters.all(), many=True).data


class CategoryDetailSerializer(serializers.ModelSerializer):
    characters = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ('id', 'name', 'characters')
    
    def get_characters(self, obj):
        return CharacterNameSerializer(obj.characters.all(), many=True).data
    
    