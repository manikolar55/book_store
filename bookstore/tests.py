import json

from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import TestCase
from .models import Author, Category, Book, ShoppingCart
from datetime import date



class AuthorTests(TestCase):

    def setUp(self):
        # Create a test user and obtain a token
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

        # Set up the API client with the token
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Create Author and Category objects
        self.author = Author.objects.create(name='Test Author')
        self.category = Category.objects.create(name='Test Category')

        self.author_data = {"name": "John Doe"}
        self.url_list = reverse('author-list')
        self.url_detail = reverse('author-detail', args=[self.author.id])

        self.category_data = {'name': 'Test Category'}
        self.cat_url_list = reverse('category-list')
        self.cat_url_detail = reverse('category-detail', args=[self.category.id])

        self.book_data = {
            'title': 'Test Book',
            'author': self.author.id,
            'published_date': str(date.today()),
            'category': self.category.id
        }

        self.book = Book.objects.create(
            title='Example Book',
            author=self.author,
            published_date=date.today(),
            category=self.category
        )

        self.book_url_list = reverse('book-list')
        self.book_url_detail = reverse('book-detail', args=[self.book.id])

        # Create ShoppingCart object
        self.shopping_cart = ShoppingCart.objects.create(user=self.user)

        self.shopping_cart_data = {
            'user': self.user.id,
            'books': [self.book.id]
        }

        self.cart_url_list = reverse('shopping_cart_list_create')
        self.cart_url_detail = reverse('shopping_cart_detail', args=[self.shopping_cart.id])

        self.pur_url = reverse('purchase')

    def test_create_author(self):
        response = self.client.post(self.url_list, data=json.dumps(self.author_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)
        self.assertEqual(Author.objects.last().name, 'John Doe')

    def test_read_author_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.author.name)

    def test_read_author_detail(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.author.name)

    def test_update_author(self):
        updated_name = 'Updated Name'
        data = {'name': updated_name}
        response = self.client.put(self.url_detail, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.name, updated_name)

    def test_delete_author(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)

    def test_create_category(self):
        response = self.client.post(self.cat_url_list, json.dumps(self.category_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.last().name, 'Test Category')

    def test_read_category_list(self):
        response = self.client.get(self.cat_url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.category.name)

    def test_read_category_detail(self):
        response = self.client.get(self.cat_url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category.name)

    def test_update_category(self):
        updated_name = 'Updated Category'
        data = {'name': updated_name}
        response = self.client.put(self.cat_url_detail, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, updated_name)

    def test_delete_category(self):
        response = self.client.delete(self.cat_url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

    def test_create_book(self):
        response = self.client.post(self.book_url_list, json.dumps(self.book_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertIsNotNone(response.data.get('isbn'))

    def test_read_book_list(self):
        response = self.client.get(self.book_url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.book.title)

    def test_read_book_detail(self):
        response = self.client.get(self.book_url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    def test_update_book(self):
        updated_title = 'Updated Book'
        data = {'title': updated_title}
        response = self.client.patch(self.book_url_detail, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, updated_title)

    def test_delete_book(self):
        response = self.client.delete(self.book_url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_create_shopping_cart(self):
        response = self.client.post(self.cart_url_list, data=json.dumps(self.shopping_cart_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShoppingCart.objects.count(), 2)
        self.assertEqual(response.data['user'], self.user.id)

    def test_read_shopping_cart_list(self):
        response = self.client.get(self.cart_url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.shopping_cart.user.id)

    def test_read_shopping_cart_detail(self):
        response = self.client.get(self.cart_url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.shopping_cart.user.id)

    def test_update_shopping_cart(self):
        updated_user = User.objects.create_user(username='updateduser', password='updatedpassword')
        data = {'user': updated_user.id, 'books': [self.book.id]}
        response = self.client.put(self.cart_url_detail, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.shopping_cart.refresh_from_db()
        self.assertEqual(self.shopping_cart.user.id, updated_user.id)

    def test_delete_shopping_cart(self):
        response = self.client.delete(self.cart_url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ShoppingCart.objects.count(), 0)

    def test_purchase_view_with_books(self):
        # Add books to the shopping cart
        self.shopping_cart.books.add(1, 2, 3)  # Assuming book IDs 1, 2, and 3

        response = self.client.get(self.pur_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Purchase successful')

        # Verify that the shopping cart is empty after purchase
        self.assertEqual(ShoppingCart.objects.filter(user=self.user).count(), 0)
