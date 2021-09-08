from rest_framework import serializers

from rest_framework.relations import SlugRelatedField

from reviews.models import Comment, Category, Genre, Title, Review


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
	genre = GenreSerializer(many=True)
	category = serializers.SlugRelatedField(slug_field='name',
		queryset=Category.objects.all())

	class Meta:
		model = Title
		fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')

	def get_rating(self, obj): # Здесь нужно будет высчитывать rating из score в БД
		return 100


class ReviewSerializer(serializers.ModelSerializer):
	author = SlugRelatedField(slug_field='username', read_only=True)

	class Meta:
		fields = ('id', 'text', 'author', 'score', 'pub_date')
		model = Review

class ReviewSerializer(serializers.ModelSerializer):
	author = SlugRelatedField(slug_field='username', read_only=True)

	class Meta:
		fields = ('id', 'text', 'author', 'score', 'pub_date')
		model = Review

class CommentSerializer(serializers.ModelSerializer):
	author = SlugRelatedField(slug_field='username', read_only=True)

	class Meta:
		fields = '__all__'
		model = Comment
