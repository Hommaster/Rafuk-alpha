from django.contrib.auth import login
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import UpdateView
from .forms import UserUpdateForm2
from .models import UserPr

menu = [
    {'title': 'home', 'url_name': 'home'},
    # {'title': '', 'url_name': ''},
    # {'title': '', 'url_name': ''},
    # {'title': '', 'url_name': ''},
]


class DataMixin(UpdateView):

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            slug = self.kwargs['users_slug']
            userpost = UserPr.objects.get(slug_field=slug)
            user_post = get_object_or_404(UserPr, slug_field=slug)
            context['password'] = user_post.password
            context['user_post'] = user_post
            if self.request.method == 'POST':
                sform = UserUpdateForm2(self.request.POST, instance=userpost)
                if sform.is_valid():
                    userpost = sform.save()
                    userpost.save()
                    context['userpost'] = userpost
                    context['get_out'] = False
            else:
                sform = UserUpdateForm2(instance=userpost)
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

    def form_valid(self, form):
        user = form.save(commit=True)
        login(self.request, user)
        return redirect('home')
