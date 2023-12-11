from django.urls import path
from auth import views as auth_views

urlpatterns = [
    path('api/register', auth_views.RegisterAPI.as_view(), name='auth.register'),
    path('api/login', auth_views.LoginAPI.as_view(), name='auth.login'),
]