# views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .tasks import send_purchase_notification
from .models import Author, Category, Book, ShoppingCart
from .serializers import AuthorSerializer, CategorySerializer, BookSerializer, ShoppingCartSerializer


class AuthorList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class CategoryList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BookList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ShoppingCartListCreateView(generics.ListCreateAPIView):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = [permissions.IsAuthenticated]


class ShoppingCartRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = [permissions.IsAuthenticated]


class PurchaseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        user_purchases = ShoppingCart.objects.filter(user=user)

        if user_purchases.exists():
            email = request.user.email
            for user_purchase in user_purchases:
                purchase_details = 'Books Purchased'
                send_purchase_notification.delay(email, purchase_details)

                user_purchase.delete()
            return Response({'message': 'Purchase successful'}, status=status.HTTP_200_OK)

        return Response({'message': 'No Book'}, status=status.HTTP_200_OK)
