# urls.py

from django.urls import path
from .views import AuthorList, AuthorDetail, CategoryList, CategoryDetail, BookList, BookDetail, PurchaseView, \
    ShoppingCartListCreateView, ShoppingCartRetrieveUpdateDestroyView

urlpatterns = [
    path('authors/', AuthorList.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetail.as_view(), name='author-detail'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    path('shopping_cart/', ShoppingCartListCreateView.as_view(), name='shopping_cart_list_create'),
    path('shopping_cart/<int:pk>/', ShoppingCartRetrieveUpdateDestroyView.as_view(), name='shopping_cart_detail'),
    path('purchase/', PurchaseView.as_view(), name='purchase'),
]
