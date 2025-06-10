from django.shortcuts import render
def home_page(request):
    return render(request,'home_page.html')

def about_autor(request):
    return render(request,'about_autor.html')

def home_goods_store(request):
    return render(request,'home_goods_store.html')
# Create your views here.
