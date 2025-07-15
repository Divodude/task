from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.user_login, name='home'),
    
    path('blog/create/', views.create_blog_post, name='create_blog_post'),
    path('blog/edit/<int:post_id>/', views.edit_blog_post, name='edit_blog_post'),
    path('blog/delete/<int:post_id>/', views.delete_blog_post, name='delete_blog_post'),
    path('blog/posts/', views.view_blog_posts, name='view_blog_posts'),
    path('blog/post/<int:post_id>/', views.blog_post_detail, name='blog_post_detail'),
]