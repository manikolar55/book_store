# urls.py

from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView

urlpatterns = [
    # ... existing paths
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
