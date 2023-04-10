from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .forms import *
from .models import *
from .utils import DataMixin


class MainHome(ListView):
    template_name = 'rafuk/home.html'
    model = Product
    paginate_by = 5
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_authenticated = self.request.user
        if self.request.user.is_authenticated:
            unap = UserPr.objects.get(username=user_authenticated)
            context['unap'] = unap
        context['title'] = 'Главная страница'
        return context


class AddPost(LoginRequiredMixin, CreateView):
    template_name = 'rafuk/addpage.html'
    form_class = AddPostForm
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('loreg')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить статью'
        return context

    def form_valid(self, form):
        form.instance.users = self.request.user
        return super().form_valid(form)


class AddUser(CreateView):
    form_class = UserCreateForm
    template_name = 'rafuk/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация пользователя'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'rafuk/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context


def logout_user(request):
    logout(request)
    return redirect('home')


def log_or_reg(request):
    return render(request, 'rafuk/log_or_reg.html', {'title': 'Отказано в доступе "Добавить статью"'})


class ProfileUser(DetailView):
    template_name = 'rafuk/profile_user.html'
    slug_url_kwarg = 'users_slug'
    context_object_name = 'profile'
    model = UserPr

    def get_object(self, queryset=None):
        slug = self.kwargs['users_slug']
        a_obj = UserPr.objects.get(slug_field=slug)
        return a_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.kwargs['users_slug']
        us = UserPr.objects.get(slug_field=name)
        context['us'] = us
        pr = Product.objects.filter(users_id=us.id)
        ruu = self.request.user.username
        pu = us.username
        if self.request.user.is_authenticated:
            if str(ruu) == str(pu):
                context['rp'] = True
            else:
                context['rp'] = False
        context['user_products'] = pr
        context['title'] = us.surname + ' ' + us.name
        return context


class ShowPost(DetailView):
    model = Product
    slug_url_kwarg = 'post_slug'
    template_name = 'rafuk/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['post_slug']
        post = Product.objects.filter(slug=slug)
        context['title'] = "Демонстрация поста"
        context['post'] = post
        return context


class SearchResultsView(ListView):
    model = Product
    template_name = 'rafuk/search_results.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Результат поиска"
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(title__icontains=query)
        return object_list


class UpdatePost2(UpdateView):
    form_class = AddPostForm
    template_name = 'rafuk/update_post.html'
    context_object_name = 'update_posts'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['title'] = 'Редактирование товара'
            slug = self.kwargs['slug']
            post = Product.objects.filter(slug=slug)
            posts = Product.objects.get(slug=slug)
            user_post = UserPr.objects.get(pk=posts.users_id)
            context['user_post'] = user_post.username
            ruu = self.request.user.username
            if str(user_post) == str(ruu):
                context['user_now'] = True
            else:
                context['user_now'] = False
            context['posts'] = posts
            context['post'] = post
            userpost = get_object_or_404(Product, slug=slug)
            context['user_post'] = userpost
            if self.request.method == 'POST':
                sform = AddPostForm(self.request.POST, instance=userpost)
                if sform.is_valid():
                    userpost = sform.save()
                    userpost.save()
                    context['userpost'] = userpost
                    context['get_out'] = False
            else:
                sform = AddPostForm(instance=userpost)
                userpost.save()
                context['sform'] = sform
                context['get_out'] = True

            return context
        else:
            context = None
            return context

    def get_object(self, queryset=None):
        return self.request.user


class DeletePost(DeleteView):
    model = Product
    template_name = 'rafuk/delete_post.html'
    context_object_name = 'tasks'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Удаление поста"
        slug = self.kwargs['slug']
        posts = Product.objects.get(slug=slug)
        context['posts'] = posts
        post_user = UserPr.objects.get(pk=posts.users_id)
        context['post_user'] = post_user.username
        ruu = self.request.user.username
        if str(post_user) == str(ruu):
            context['user_now'] = True
        else:
            context['user_now'] = False
        userpost = get_object_or_404(Product, slug=slug)
        context['user_post'] = userpost
        return context

    def form_valid(self, form):
        messages.success(self.request, "Удаление поста прошло успешно!")
        return super(DeletePost, self).form_valid(form)


class UpdateProfile(DataMixin, UpdateView):
    form_class = UserUpdateForm2
    slug_url_kwarg = 'users_slug'
    template_name = 'rafuk/update_profile.html'
    success_url = reverse_lazy('home')
    context_object_name = 'update_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение данных профиля'
        return context

    def get_object(self, queryset=None):
        slug = self.kwargs['users_slug']
        a_obj = UserPr.objects.get(slug_field=slug)
        return a_obj


class ChangePassword(DataMixin, UpdateView):
    form_class = ChangePasswordForm
    template_name = 'rafuk/change_password.html'
    success_url = reverse_lazy('home')
    slug_url_kwarg = 'users_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Смена пароля'
        return context

    def get_object(self, queryset=None):
        slug = self.kwargs['users_slug']
        a_obj = UserPr.objects.get(slug_field=slug)
        return a_obj


class SearchResultsEmail(ListView):
    model = UserPr
    template_name = 'rafuk/change_password_na.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Результат поиска пользователя'
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = UserPr.objects.filter(email__icontains=query)
        return object_list


def search_email(request):
    return render(request, 'rafuk/search_email.html', {'title': 'Результат поиска аккаунта'})


class ChangePasswordNA(UpdateView):
    form_class = ChangePasswordForm
    slug_url_kwarg = 'users_slug'
    template_name = 'rafuk/change_password_naAA.html'
    success_url = reverse_lazy('home')
    context_object_name = 'update_password_na'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация нового пароля'
        slug = self.kwargs['users_slug']
        userpost = UserPr.objects.get(slug_field=slug)
        user_post = get_object_or_404(UserPr, slug_field=slug)
        context['user_post'] = user_post
        if self.request.method == 'POST':
            sform = ChangePasswordForm(self.request.POST, instance=userpost)
            if sform.is_valid():
                userpost = sform.save()
                userpost.save()
                context['userpost'] = userpost
                context['get_out'] = False
        else:
            sform = ChangePasswordForm(instance=userpost)
            userpost.save()
            context['sform'] = sform
            context['get_out'] = True
        ruu = self.request.user.username
        context['userpost'] = userpost.username
        if str(userpost) == str(ruu):
            context['user_now'] = True
        else:
            context['user_now'] = False
        return context

    def get_object(self, queryset=None):
        slug = self.kwargs['users_slug']
        a_obj = UserPr.objects.get(slug_field=slug)
        return a_obj
