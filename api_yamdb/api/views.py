from django.shortcuts import get_list_or_404
from rest_framework import viewsets, mixins, filters
from django.shortcuts import get_object_or_404
from django_filters import FilterSet, CharFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import get_object_or_404

from .serializers import TitleSerializer, GenreSerializer, CategorySerializer, ReviewSerializer, CommentSerializer
from .permissions import IsAdminOrReadOnly
from reviews.models import Comment, Review, Title, Genre, Category, GenreTitle


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
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(CreateListDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def perform_create(self, serializer):
        category = get_object_or_404(Category,
            slug=serializer.initial_data.get('category'))
        genre_slug = serializer.initial_data.get('genre')
        serializer.save(category=category)
        genre_slug = serializer.initial_data.get('genre')
        title_id = get_object_or_404(Title,
                                     name=serializer.initial_data.get('name'))
        for slug in genre_slug:
            GenreTitle.objects.create(
                genre_id=get_object_or_404(Genre, slug=slug),
                title_id=title_id
            )


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
