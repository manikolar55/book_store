# views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .tasks import send_purchase_notification
from .models import Author, Category, Book, ShoppingCart
from .serializers import AuthorSerializer, CategorySerializer, BookSerializer, ShoppingCartSerializer


class AuthorList(generics.ListCreateAPIView):
    """
        API endpoint for listing and creating authors.

        Permissions:
        - Only authenticated users are allowed.

        HTTP Methods:
        - GET: Retrieve a list of authors.
        - POST: Create a new author.

        Serializer:
        - AuthorSerializer: Serializes Author model data.
        """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    """
        API endpoint for retrieving, updating, and deleting an author.

        Permissions:
        - Only authenticated users are allowed.

        HTTP Methods:
        - PUT: Update details of a specific author.
        - PATCH: Partially update details of a specific author.
        - DELETE: Delete a specific author.

        Serializer:
        - AuthorSerializer: Serializes Author model data.
        """
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
    """
       API endpoint for listing and creating shopping carts.

       Permissions:
       - Only authenticated users are allowed.

       HTTP Methods:
       - GET: Retrieve a list of shopping carts.
       - POST: Create a new shopping cart.

       Serializer:
       - ShoppingCartSerializer: Serializes ShoppingCart model data.
       """
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = [permissions.IsAuthenticated]


class ShoppingCartRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
       API endpoint for retrieving, updating, and deleting a shopping cart.

       Permissions:
       - Only authenticated users are allowed.

       HTTP Methods:
       - GET: Retrieve details of a specific shopping cart.
       - PUT: Update details of a specific shopping cart.
       - PATCH: Partially update details of a specific shopping cart.
       - DELETE: Delete a specific shopping cart.

       Serializer:
       - ShoppingCartSerializer: Serializes ShoppingCart model data.
       """
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = [permissions.IsAuthenticated]


class PurchaseView(APIView):
    """
        API endpoint for making a purchase.

        Permissions:
        - Only authenticated users are allowed.

        HTTP Method:
        - GET: Perform a purchase, send a notification, and empty the shopping cart.

        Returns:
        - 200 OK: If the purchase is successful or there are no books in the cart.
        - Response({'message': 'Purchase successful'}): If the purchase is successful.
        - Response({'message': 'No Book'}): If there are no books in the cart.
    """
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
