from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    about_yourself = models.TextField(blank=True, null=True,verbose_name="о себе", max_length=200)

class Category(models.Model):
    name = models.CharField(verbose_name='название', max_length=100)
    description = models.TextField(verbose_name='описание', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

class Product(models.Model):
    name=models.CharField(verbose_name='название', max_length=200)
    description = models.TextField(verbose_name='описание', blank=True, null=True)
    photo_product = models.ImageField(verbose_name='фото', blank=True, null=True,upload_to="media/")
    price= models.DecimalField( verbose_name='цена',max_digits=10,decimal_places=2,validators=[MinValueValidator(0)])
    quantity_in_stock = models.IntegerField(verbose_name='количество_на_складе',validators=[MinValueValidator(0)])
    category = models.ForeignKey('Category',on_delete=models.CASCADE,verbose_name='категория')
    maker=models.ForeignKey('Maker',on_delete=models.CASCADE,verbose_name='производитель')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

class Maker(models.Model):
    name = models.CharField(verbose_name='название', max_length=100)
    country=models.CharField(verbose_name='страна', max_length=100)
    description = models.TextField(verbose_name='описание', blank=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "производитель"
        verbose_name_plural = "производители"

class Basket(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,verbose_name='пользователь')
    creation_date = models.DateTimeField(auto_now_add= True,verbose_name="дата создания")

    def __str__(self):
        return f"Корзина пользователя <{self.user.username}>"
    
    def total_cost(self):
        return sum(item.element_cost() for item in self.basket_elem.all())
    
    total_cost.short_description ='общая стоимость' # для нормального отображения в админке

    class Meta:
        verbose_name = "корзина"
        verbose_name_plural = "корзины"

class Basket_elem(models.Model):
    basket = models.ForeignKey(Basket,on_delete=models.CASCADE,verbose_name="корзина",related_name='basket_elem') 
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="товар")
    quantity = models.PositiveIntegerField(verbose_name="Кколичество")

    def __str__(self):
        return f"{self.product.name}({self.quantity} шт.)"
    
    class Meta:
        verbose_name = "элемент корзины"
        verbose_name_plural = "элементы корзины"
    
    def element_cost(self):
        return self.product.price * self.quantity
    
    element_cost.short_description ='стоимость элемента'

    def clean(self):
        if self.quantity > self.product.quantity_in_stock:
            raise ValidationError(
                "Недостаточно товара на складе. Доступно: {self.product.quantity_in_stock}"
            )

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,verbose_name="Пользователь")
    created = models.DateTimeField(auto_now_add=True,verbose_name="Дата создания")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")

    def __str__(self):
        return f"Заказ пользователя <{self.user.username}>"
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE,verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"

# Create your models here.