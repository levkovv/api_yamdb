from rest_framework import viewsets, mixins, filters
from django.shortcuts import get_object_or_404
from django_filters import FilterSet, CharFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import TitleSerializer, GenreSerializer, CategorySerializer, ReviewSerializer, CommentSerializer
from reviews.models import Comment, Review, Title, Genre, Category


class CreateListDeleteViewSet(mixins.CreateModelMixin,
							  mixins.ListModelMixin,
							  mixins.DestroyModelMixin,
							  viewsets.GenericViewSet):
	pass


class TitleFilter(FilterSet):
	category = CharFilter(field_name='category__slug', lookup_expr='exact')
	genre = CharFilter(field_name='genre__slug', lookup_expr='exact')

	class Meta:
		model = Title
		fields = ('name', 'year', 'genre', 'category')


class CategoryViewSet(CreateListDeleteViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	lookup_field = 'slug'
	filter_backends = (filters.SearchFilter,)
	search_fields = ('name',)
	# permission_classes =
	# pagination_class =


class GenreViewSet(CreateListDeleteViewSet):
	queryset = Genre.objects.all()
	serializer_class = GenreSerializer
	lookup_field = 'slug'
	filter_backends = (filters.SearchFilter,)
	search_fields = ('name',)
	# permission_classes =
	# pagination_class =
	# search_fields


class TitleViewSet(viewsets.ModelViewSet):
	queryset = Title.objects.all()
	serializer_class = TitleSerializer
	filter_backends = (DjangoFilterBackend,)
	filterset_class = TitleFilter
	# permission_classes =
	# pagination_class =


class ReviewViewSet(viewsets.ModelViewSet):
	serializer_class = ReviewSerializer

	def get_queryset(self):
		title = get_object_or_404(
			Title,
			id=self.kwargs.get('id')
		)
		return title.comments.all()

class CommentViewSet(viewsets.ModelViewSet):
	serializer_class = CommentSerializer

	def get_queryset(self):
		review = get_object_or_404(
			Review,
			title_id=self.kwargs.get('id'),
			id=self.kwargs.get('review_id')
		)
		return review.comments.all()

