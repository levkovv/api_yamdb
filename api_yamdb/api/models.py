from django.db import models


class Category(models.Model):
	name = models.CharField(max_length=256)
	slug = models.SlugField(max_length=50, unique=True)

	def __str__(self):
		return self.name


class Genre(models.Model):
	name = models.CharField(max_length=256)
	slug = models.SlugField(max_length=50, unique=True)

	def __str__(self):
		return self.name


class Title(models.Model):
	name = models.CharField(max_length=256)
	year = models.SmallIntegerField()
	description = models.TextField(blank=True, null=True)
	genre = models.ManyToManyField(Genre, through='GenreTitle')
	category = models.ForeignKey(Category, related_name='titles',
		on_delete=models.SET_NULL, blank=True, null=True)
	
	def __str__(self):
		return self.name


class GenreTitle(models.Model):
	title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
	genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.title_id} {self.genre_id}'
