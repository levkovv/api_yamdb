from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from reviews.models import Category, Genre, Title, Review


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, read_only=True)
    category = serializers.SlugRelatedField(slug_field='slug',
        read_only=True)
    
    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
    
    def get_rating(self, obj): # Здесь нужно будет высчитывать rating из score в БД
        return 100
 