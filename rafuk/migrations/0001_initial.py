# Generated by Django 4.1.7 on 2023-04-05 11:38

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=100, verbose_name='Имя пользователя')),
                ('surname', models.CharField(max_length=100, verbose_name='Фамиля')),
                ('patronymic', models.CharField(max_length=100, verbose_name='Отчество')),
                ('slug_field', models.SlugField(max_length=100, verbose_name='URL-адрес пользователя')),
                ('date_of_birth', models.DateTimeField(null=True, verbose_name='Дата рождения')),
                ('phone_number', models.IntegerField(null=True, verbose_name='номер телефона')),
                ('place', models.TextField(max_length=150, null=True, verbose_name='Адрес проживания')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователь',
                'ordering': ['name'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Категория товара')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL-категории')),
            ],
            options={
                'verbose_name': 'Категория товаров',
                'verbose_name_plural': 'Категория товаров',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Where',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Города Беларуси')),
            ],
            options={
                'verbose_name': 'Города Беларуси',
                'verbose_name_plural': 'Города Беларуси',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Наименование товара')),
                ('slug', models.SlugField(max_length=250, unique=True, verbose_name='URL-адрес товара')),
                ('price', models.IntegerField(verbose_name='Стоимость')),
                ('content', models.TextField(blank=True, verbose_name='Описание')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления поста')),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Изображение товара')),
                ('is_published', models.BooleanField(default=True, verbose_name='Публикация')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rafuk.categories', verbose_name='Категория товара')),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('where', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rafuk.where', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товар',
                'ordering': ['time_create'],
            },
        ),
    ]
