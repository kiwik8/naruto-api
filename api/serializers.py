from rest_framework import serializers
from api.models import Character, Category
from api.pagination import ClassicPagination



class CharacterNameSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    class Meta():
        
        model = Character
        fields = ('id', 'name')

    def get_name(self, obj):
        return obj.fr_name

class CategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CharacterListSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    fr_categories = serializers.SerializerMethodField()


    class Meta:
        model = Character
        fields = ('id', 'name', 'description', 'image', 'fr_categories')

    def __init__(self, *args, **kwargs):
        language = kwargs.pop('language', None)
        self.language = language
        #fields = variables.get_fields(language, 1) 
        super(CharacterListSerializer, self).__init__(*args, **kwargs)
        if self.language == 'en':
            self.fields.pop('fr_categories')


    def get_name(self, obj):
        if self.language == 'fr':
            return obj.fr_name
        elif self.language == 'en':
            return obj.en_name
        
    def get_description(self, obj):
        if self.language == 'fr':
            return obj.fr_description
        elif self.language == 'en':
            return obj.en_description

    def get_id(self, obj):
        return obj.id

    def get_image(self, obj):
        return obj.image


    def get_fr_categories(self, obj):
        return CategoryNameSerializer(obj.fr_categories.all(), many=True).data





class CharacterDetailSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='fr_name')
    description = serializers.CharField(source='fr_description')
    general_infos = serializers.CharField(source='fr_general_infos')
    fr_categories = serializers.SerializerMethodField()

    class Meta:
        model = Character
        fields = ('id', 'name', 'description', 'image', 'general_infos', 'fr_categories')

    def __init__(self, *args, **kwargs):
        language = kwargs.pop('language', None)
        self.language = language
        super(CharacterDetailSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, instance):
        if self.language == 'en':
            self.fields.pop('fr_categories')
            name = instance.en_name
            description = instance.en_description
            general_infos = instance.en_general_infos
        elif self.language == 'fr':
            name = instance.fr_name
            description = instance.fr_description
            general_infos = instance.fr_general_infos
        rep = super().to_representation(instance)
        rep['name'] = name
        rep['description'] = description
        rep['general_infos'] = general_infos
        return rep


    def get_fr_categories(self, obj):
        return CategoryNameSerializer(obj.fr_categories.all(), many=True).data

    



class CategoryListSerializer(serializers.ModelSerializer):

    characters = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'characters')

    def __init__(self, *args, **kwargs):
        super(CategoryListSerializer, self).__init__(*args, **kwargs)

    def get_characters(self, obj):
        return CharacterNameSerializer(obj.characters.all(), many=True).data


class CategoryDetailSerializer(serializers.ModelSerializer):
    characters = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ('id', 'name', 'characters')

    
    def get_characters(self, obj):
        return CharacterNameSerializer(obj.characters.all(), many=True).data
    
    