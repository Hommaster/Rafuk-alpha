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


# class UserUpdateForm(UserCreationForm):
#     username = forms.CharField(label='Логин')
#     name = forms.CharField(label='Имя')
#     email = forms.EmailField(label='Почтовый адрес')
#     surname = forms.CharField(label='Фамилия')
#     patronymic = forms.CharField(label='Отчество')
#     date_of_birth = forms.DateTimeField(label='Дата рождения')
#     phone_number = forms.IntegerField(label='Номер телефона')
#     password1 = forms.CharField(label='Пароль')
#     password2 = forms.CharField(label='Повторите пароль')


class UserUpdateForm2(forms.ModelForm):
    name = forms.CharField(label='Имя')
    email = forms.EmailField(label='Адрес электронной почты')
    surname = forms.CharField(label='Фамилия')
    patronymic = forms.CharField(label='Отчество')

    class Meta:
        model = UserPr
        fields = ('name', 'surname', 'patronymic', 'phone_number', 'email')


class ChangePasswordForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Новый пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')

    class Meta:
        model = UserPr
        fields = ('password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    email = forms.EmailField(label='Почтовый адрес')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'content', 'photo', 'is_published', 'where', 'cat']
