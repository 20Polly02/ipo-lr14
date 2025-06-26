from django.shortcuts import render
import json
from django.http import JsonResponse #новое
from django.contrib.auth.decorators import login_required # новое
from django.views.decorators.http import require_POST #новое
from django.contrib.auth import login, authenticate #новое
from .forms import UserRegistrationForm, LoginForm #новое
from .models import Product,Category,Maker,Basket,Basket_elem
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import Filter
def home_page(request):
    return render(request,'home_page.html')

def about_autor(request):
    return render(request,'about_autor.html')

def home_goods_store(request):
    return render(request,'home_goods_store.html')
def speciality(request):
    specialities=[]
    with open("data/dump.json", 'r', encoding='utf-8') as file:  
        info_file = json.load(file)
    for specialty in info_file:  
        if specialty.get("model") == "data.specialty": 
            speciality = {
                "code": specialty["fields"].get("code"),
                "pk": specialty.get("pk"), 
                "title" : specialty["fields"].get("title"),  
                "c_type": specialty["fields"].get("c_type")  
            }
            specialities.append(speciality)
    return render(request,'speciality.html',{'specialities':specialities})
def speciality_found(request):
    c = request.GET.get('c')
    speciality = []  
    with open("data/dump.json", 'r', encoding='utf-8') as file:
        read_file = json.load(file)
        for specialty in read_file:
            if specialty.get("model") == "data.specialty":
                if specialty["fields"].get("code") == c:
                    specialty_f = {
                        "code": specialty["fields"].get("code"),
                        "pk": specialty.get("pk"),
                        "title": specialty["fields"].get("title"),
                        "educational": specialty["fields"].get("c_type"),
                    }
                    speciality.append(specialty_f)  

    return render(request, "speciality_found.html", {'speciality': speciality})

def speciality_id(request,id):
    speciality = []  
    with open("data/dump.json", 'r', encoding='utf-8') as file:
        read_file = json.load(file)
        for specialty in read_file:
            if specialty.get("model") == "data.specialty":
                if int(specialty.get("pk")) == int(id):
                    specialty_i= {
                        "code": specialty["fields"].get("code"),
                        "pk": specialty.get("pk"),
                        "title": specialty["fields"].get("title"),
                        "educational": specialty["fields"].get("c_type"),
                    }
                    speciality.append(specialty_i)  

    return render(request, "speciality_found.html", {'speciality': speciality}) 
def product_list(request):
    products = Product.objects.all()
    search_query = request.GET.get('search', '')
    
    # Применяем поиск, если есть запрос
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    # Применяем другие фильтры
    form = Filter(request.GET or None)
    if form.is_valid():
        if form.cleaned_data['category']:
            products = products.filter(category__name__iexact=form.cleaned_data['category'])
        if form.cleaned_data['maker']:
            products = products.filter(maker__name__iexact=form.cleaned_data['maker'])
    
    return render(request, 'shop/product_list.html', {
        'products': products,
        'form': form,
        'categories': Category.objects.all(),  # Добавьте это
        'makers': Maker.objects.all()         # И это
    })
def product_detail(request,id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        messages.error(request, "Товар не найден.")
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required

def add_product_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist or  UnboundLocalError :
        messages.error(request, "Товар не найден.")
        return redirect('cart_user')
    basket, created = Basket.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    basket_element, created = Basket_elem.objects.get_or_create(
        basket=basket,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        basket_element.quantity += quantity
        basket_element.save()
        messages.success(request, "Количество товара обновлено в корзине.")
    else:
        messages.success(request, "Товар добавлен в корзину.")
    return redirect('cart_user')

@login_required
@require_POST

def update_cart(request, item_id):
    try:
        basket_element = Basket_elem.objects.get(id=item_id, basket__user=request.user)
    except Basket_elem.DoesNotExist:
        messages.error(request, "Не удалось обновить корзину")
        return redirect('cart_user')

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    if quantity <= 0:
        basket_element.delete()
        messages.success(request, "Товар удалён из корзины")
    elif quantity <= basket_element.product.quantity_in_stock:
        basket_element.quantity = quantity
        basket_element.save()
        messages.success(request, "Количество товара обновлено")
    else:
        messages.error(request, "Недостаточно товара на складе")

    return redirect('cart_user')

@login_required

def remove_from_cart(request, item_id):
    try:
        basket_element = Basket_elem.objects.get(id=item_id, basket__user=request.user)
        basket_element.delete()
        messages.success(request, "Товар удалён из корзины")
    except Basket_elem.DoesNotExist:
        messages.error(request, "Товар не найден в корзине")
    return redirect('cart_user')
    
@login_required

def cart_user(request):
    basket, created = Basket.objects.get_or_create(user=request.user)
    basket_elements = basket.basket_elem.select_related('product').all()
    total = sum(item.element_cost() for item in basket_elements)
    context = {
        'cart_items': basket_elements,
        'total': total,
    }
    return render(request, 'shop/cart.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cart_user')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('cart_user')
    else:
        form = LoginForm()
    return render(request, 'login_user.html', {'form': form})
# Create your views here.
