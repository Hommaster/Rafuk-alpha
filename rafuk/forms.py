from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import UserPr, Product


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'content', 'photo', 'is_published', 'where', 'cat']


class UserCreateForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    name = forms.CharField(label='Имя')
    email = forms.EmailField(label='Почтовый адрес')
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Повторите пароль')
    surname = forms.CharField(label='Фамилия')
    patronymic = forms.CharField(label='Отчество')
    date_of_birth = forms.DateTimeField(label='Дата рождения')
    phone_number = forms.IntegerField(label='Номер телефона')

    class Meta:
        model = UserPr
        fields = ('username', 'name', 'surname', 'patronymic', 'date_of_birth',
                  'phone_number', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    email = forms.EmailField(label='Почтовый адрес')
    password = forms.CharField(label='Пароль')


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'content', 'photo', 'is_published', 'where', 'cat']