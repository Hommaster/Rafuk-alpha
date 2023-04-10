from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import PROTECT
from django.urls import reverse

from .templates.slugify import slugify


class Product(models.Model):
    title = models.CharField(max_length=250, verbose_name='Наименование товара')
    slug = models.SlugField(max_length=250, db_index=True, unique=True, verbose_name='URL-адрес товара')
    price = models.IntegerField(verbose_name='Стоимость')
    content = models.TextField(blank=True, verbose_name='Описание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата '
                                                                       'создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления поста')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name=''
                                                                        'Изображение товара')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    where = models.ForeignKey('Where', on_delete=PROTECT, verbose_name='Город')
    cat = models.ForeignKey('Categories', on_delete=PROTECT, verbose_name='Категория товара')
    users = models.ForeignKey('UserPr', on_delete=PROTECT, verbose_name='Пользователь')

    def save(self, *args, **kwargs):
        super(Product, self).save()
        if not self.slug:
            self.slug = slugify(self.title) + '-' + str(self.pk)
            super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товар'
        ordering = ['time_create']


class Where(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Города Беларуси')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Города Беларуси'
        verbose_name_plural = 'Города Беларуси'
        ordering = ['name']


class Categories(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Категория товара')
    slug = models.SlugField(max_length=100, db_index=True, unique=True, verbose_name='URL-категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категория товаров'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('cats', kwargs={'cat_slug': self.slug})


class UserPr(AbstractUser):
    name = models.CharField(max_length=100, verbose_name='Имя пользователя')
    surname = models.CharField(max_length=100, verbose_name='Фамиля')
    patronymic = models.CharField(max_length=100, verbose_name='Отчество')
    slug_field = models.SlugField(max_length=100, verbose_name='URL-адрес пользователя')
    date_of_birth = models.DateTimeField(null=True, verbose_name='Дата рождения')
    phone_number = models.IntegerField(null=True, verbose_name='номер телефона')
    place = models.TextField(null=True, max_length=150, verbose_name='Адрес проживания')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'
        ordering = ['name']

    def save(self, *args, **kwargs):
        super(UserPr, self).save()
        if not self.slug_field:
            self.slug_field = slugify(self.username) + '-' + str(self.pk)
            super(UserPr, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users', kwargs={'users_slug': self.slug_field})

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
