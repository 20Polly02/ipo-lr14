from django.urls import path
from .views import home_page, about_autor, home_goods_store, speciality, speciality_id, speciality_found,product_list,product_detail,cart_user,add_product_cart,update_cart,remove_from_cart,user_login,register

urlpatterns = [
    path('', home_page, name='home_page'),
    path('about_autor', about_autor, name='about_autor'),
    path('home_goods_store', home_goods_store, name='home_goods_store'),
    path('spec', speciality, name='speciality'),
    path('spec/<int:id>/', speciality_id, name='speciality_id'),
    path('speciality_found', speciality_found, name='speciality_found'),

    path('catalog',product_list, name='catalog'),#список товаров (каталог)
    path('catalog/<int:id>/',product_detail,name='product_detail'),#детальная информация о товаре по его ID.
    path('cart/', cart_user,name= 'cart_user'),#просмотр корзины пользователя
    path('cart/add/<int:product_id>/',add_product_cart,name='add_product_cart'),#добавление товара в корзину
    path('cart/update/<int:item_id>/',update_cart,name='update_cart'),#обновление количества товара в корзине.
    path('cart/remove/<int:item_id>/',remove_from_cart,name='remove_from_cart'),#удаление товара из корзины.

    path('register/', register, name='register'),
    path('login/', user_login, name='login_user'),
]