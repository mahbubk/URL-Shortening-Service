
from django.urls import path
from .views import index, redirect_url, register, user_login, user_logout, user_links

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('user/links/', user_links, name='user_links'),
    path('<str:short_code>/', redirect_url, name='redirect_original'),
]