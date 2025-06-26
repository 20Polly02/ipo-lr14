from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from .models import Category, Maker, Product, Basket,Basket_elem
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdminModel(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name","description")

@admin.register(Maker)
class MakerAdminModel(admin.ModelAdmin):
    list_display = ("name", "country")
    search_fields = ("name", "country")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo_product', 'price', 'quantity_in_stock', 'category', 'maker')
    list_filter = ('category', 'maker')
    search_fields = ('name', 'description')
    
    def display_photo(self, obj): 
        if obj.photo_product:
            return format_html(                                                                            
                '<img src="{}" width="70" height="70" style="object-fit: contain; background: #f0f0f0;" />', #object-fit: contain - сохраняет пропорции, помещая всё изображение в заданные размеры
                obj.photo_product.url 
            )
        return "—"
    display_photo.short_description = 'Фото'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email']
    fieldsets = (
         
        ('Персональная информация', {
            'fields': ('username','first_name', 'last_name','about_yourself','email','password')
        }),
        
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2')
        }),
    )


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'creation_date', 'total_cost',)
    list_filter = ('creation_date',)
    search_fields = ('user__username',)
    readonly_fields = ('creation_date', 'total_cost',) 
    fieldsets = (
            (None, {
                'fields': ('user', 'creation_date', 'total_cost')
            }),
        )


@admin.register(Basket_elem)
class BasketElementAdmin(admin.ModelAdmin):
    list_display = ('basket', 'product', 'quantity', 'element_cost',)
    list_filter = ('basket__user', 'product',)
    search_fields = ('product__name', 'basket__user__username',)
    readonly_fields = ('element_cost',)
    
    fieldsets = (
        (None, {
            'fields': ('basket', 'product', 'quantity')
        }),
    )