from django.urls import path
from .views import home_page, about_autor, home_goods_store, speciality, speciality_id, speciality_found

urlpatterns = [
    path('', home_page, name='home_page'),
    path('about_autor', about_autor, name='about_autor'),
    path('home_goods_store', home_goods_store, name='home_goods_store'),
    path('spec', speciality, name='speciality'),
    path('spec/<int:id>/', speciality_id, name='speciality_id'),
    path('speciality_found', speciality_found, name='speciality_found'),
]