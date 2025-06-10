from django.urls import path
from .views import home_page, about_autor, home_goods_store

urlpatterns = [
    path('', home_page, name='home_page'),
    path('about_autor', about_autor, name='about_autor'),
    path('home_goods_store', home_goods_store, name='home_goods_store'),
]