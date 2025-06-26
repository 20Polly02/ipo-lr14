from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,AuthenticationForm # для аутентификации последняя

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email','about_yourself')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class Filter(forms.Form):
    category = forms.CharField(required=False, label='Категория')
    maker = forms.CharField(required=False,label='Производитель')
    search = forms.CharField(required=False, label='Поиск')

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','first_name', 'last_name','about_yourself','email','password1','password2')

class LoginForm(AuthenticationForm):
    pass