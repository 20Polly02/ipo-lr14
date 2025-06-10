from django.shortcuts import render
import json
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

# Create your views here.
