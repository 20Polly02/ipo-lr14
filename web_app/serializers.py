from rest_framework import serializers
from .models import Product,Category,Maker,Basket,Basket_elem,Order,OrderItem

class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MakerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maker
        fields = '__all__'

class BasketModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = '__all__'
    
class Basket_elementModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket_elem
        fields = '__all__'

class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'