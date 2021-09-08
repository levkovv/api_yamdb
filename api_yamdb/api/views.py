from rest_framework import viewsets, mixins, filters

from django_filters import FilterSet, CharFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import TitleSerializer, GenreSerializer, CategorySerializer
from reviews.models import Title, Genre, Category


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
