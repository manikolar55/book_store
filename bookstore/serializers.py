# serializers.py
import random

from rest_framework import serializers
from .models import Author, Category, Book, ShoppingCart


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['isbn']

    def create(self, validated_data):
        # Generate a unique ISBN during creation
        while True:
            generated_isbn = str(random.randint(1000000, 999999999999))  # Change this range based on your requirements
            if not Book.objects.filter(isbn=generated_isbn).exists():
                break

        validated_data['isbn'] = generated_isbn
        return super().create(validated_data)


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'
