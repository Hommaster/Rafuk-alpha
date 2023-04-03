from django.urls import path

from .views import*

urlpatterns = [
    path('', MainHome.as_view(), name='home'),
    path('addpage/', AddPost.as_view(), name='AddPost'),
    path('register/', AddUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('log_or_reg/', log_or_reg, name='loreg'),
    path('user/<slug:users_slug>/', ProfileUser.as_view(), name='users'),
    path('posts/<slug:post_slug>/', ShowPost.as_view(), name='posts'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('update/post/<slug:slug>/', UpdatePost2.as_view(), name='UpdatePost'),
    path('delete/post/<slug:slug>/', DeletePost.as_view(), name='Delete_Post'),
    path('update/profile/<slug:users_slug>/', UppdateProfile.as_view(), name='Update_Profile'),
]
