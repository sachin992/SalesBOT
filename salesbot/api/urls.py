from django.urls import path
from .views import query_view
from .views import RegisterView, LoginView, ChatView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
path('query/', query_view, name='query'),
path('register/', RegisterView.as_view(), name='register'),
path('login/', LoginView.as_view(), name='login'),  
path('chat/', ChatView.as_view(), name='chat'),
path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]