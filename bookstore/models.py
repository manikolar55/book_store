# models.py

from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class ShoppingCart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
