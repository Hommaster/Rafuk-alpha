from django.urls import path
from django.views.decorators.cache import cache_page

from .views import*

urlpatterns = [
    path('', MainHome.as_view(), name='home'),
    path('addpage/', AddPost.as_view(), name='AddPost'),
    path('register/', AddUser.as_view(), name='register'),
    path('accounts/login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('log_or_reg/', log_or_reg, name='loreg'),
    path('user/<slug:users_slug>/', ProfileUser.as_view(), name='users'),
    path('posts/<slug:post_slug>/', cache_page(70)(ShowPost.as_view()), name='posts'),
    path('search/', cache_page(20)(SearchResultsView.as_view()), name='search_results'),
    path('update/post/<slug:slug>/', UpdatePost2.as_view(), name='UpdatePost'),
    path('delete/post/<slug:slug>/', DeletePost.as_view(), name='Delete_Post'),
    path('update/profile/<slug:users_slug>/', UpdateProfile.as_view(), name='Update_Profile'),
    path('update/password/<slug:users_slug>/', ChangePassword.as_view(), name='Change_Password'),
    path('update/search/password/<slug:users_slug>/', ChangePasswordNA.as_view(), name='Change_Password_NA'),
    path('searchemail/results/', SearchResultsEmail.as_view(), name='search_results_email'),
    path('searchemail/', search_email, name='search_email'),
]
