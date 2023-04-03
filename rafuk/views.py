from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .forms import *
from .models import *
from .utils import DataMixin


class MainHome(DataMixin, ListView):
    template_name = 'rafuk/home.html'
    model = Product
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_authenticated = self.request.user
        if self.request.user.is_authenticated:
            unap = UserPr.objects.get(username=user_authenticated)
            context['unap'] = unap
        c_df = self.get_context_user(title='Главная страница')
        return dict(list(context.items())+list(c_df.items()))


class AddPost(DataMixin, LoginRequiredMixin, CreateView):
    template_name = 'rafuk/addpage.html'
    form_class = AddPostForm
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('loreg')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_df = self.get_context_user(title='Добавить статью')
        return dict(list(context.items()) + list(c_df.items()))

    def form_valid(self, form):
        form.instance.users = self.request.user
        return super().form_valid(form)


class AddUser(DataMixin, CreateView):
    form_class = UserCreateForm
    template_name = 'rafuk/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_df = self.get_context_user(title='Регистрация пользователя')
        return dict(list(context.items()) + list(c_df.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'rafuk/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_df = self.get_context_user(title='Авторизация')
        return dict(list(context.items()) + list(c_df.items()))


def logout_user(request):
    logout(request)
    return redirect('home')


def log_or_reg(request):
    return render(request, 'rafuk/log_or_reg.html', {'title': 'Отказано в доступе "Добавить статью"'})


class ProfileUser(DataMixin, DetailView):
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
        c_df = self.get_context_user(user_products=pr, title=us.surname + ' ' + us.name)
        return dict(list(context.items()) + list(c_df.items()))


class ShowPost(DataMixin, DetailView):
    model = Product
    slug_url_kwarg = 'post_slug'
    template_name = 'rafuk/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['post_slug']
        post = Product.objects.filter(slug=slug)
        c_df = self.get_context_user(title="Демонстрация поста", post=post)
        return dict(list(context.items()) + list(c_df.items()))


class SearchResultsView(DataMixin, ListView):
    model = Product
    template_name = 'rafuk/search_results.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_df = self.get_context_user(title="Результат поиска")
        return dict(list(context.items()) + list(c_df.items()))

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(title__icontains=query)
        return object_list


class UpdatePost2(DataMixin, UpdateView):
    form_class = AddPostForm
    template_name = 'rafuk/update_post.html'
    context_object_name = 'update_posts'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            c_df = self.get_context_user(title='Редактирование товара')
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

            return dict(list(context.items()) + list(c_df.items()))
        else:
            context = None
            return context

    def get_object(self, queryset=None):
        return self.request.user


class DeletePost(DataMixin, DeleteView):
    model = Product
    template_name = 'rafuk/delete_post.html'
    context_object_name = 'tasks'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_df = self.get_context_user(title="Удаление поста")
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
        return dict(list(context.items()) + list(c_df.items()))

    def form_valid(self, form):
        messages.success(self.request, "Удаление поста прошло успешно!")
        return super(DeletePost, self).form_valid(form)


class UppdateProfile(UpdateView):
    form_class = UserCreateForm
    slug_url_kwarg = 'users_slug'
    template_name = 'rafuk/update_profile.html'
    success_url = reverse_lazy('login')
    context_object_name = 'update_profile'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            slug = self.kwargs['users_slug']
            userpost = UserPr.objects.get(slug_field=slug)
            user_post = get_object_or_404(UserPr, slug_field=slug)
            context['user_post'] = user_post
            if self.request.method == 'POST':
                sform = UserCreateForm(self.request.POST, instance=userpost)
                if sform.is_valid():
                    userpost = sform.save()
                    userpost.save()
                    context['userpost'] = userpost
                    context['get_out'] = False
            else:
                sform = UserCreateForm(instance=userpost)
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
        else:
            context = None
            return context

    def get_object(self, queryset=None):
        slug = self.kwargs['users_slug']
        a_obj = UserPr.objects.get(slug_field=slug)
        return a_obj

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')