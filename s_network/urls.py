"""
URL configuration for s_network project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from network.users import login_view, logout_view, register, login_is_required, profile_view, users_view, edit_profile
from network.views import home, PostView, view_posts, comments_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('login_required/', login_is_required, name='login_required'),
    path('register/', register, name='register'),
    path('', home, name='home'),
    path('profile/<int:user_id>/', profile_view, name='profile'),
    path('users/', users_view, name='users'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('posts/', view_posts, name='view_posts'),
    path('posts/users/<int:social_user_id>/', view_posts, name='view_posts'),
    path('post/', PostView.as_view(), name='create_post'),
    path('post/<int:post_id>/', PostView.as_view(), name='post_view'),
    path('comments/', comments_view, name='comments'),
    path('comments/user/<int:social_user_id>/', comments_view, name='user_comments'),
    path('comments/post/<int:post_id>/', comments_view, name='comments'),    


]
