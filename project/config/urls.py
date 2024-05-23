"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from app.views import *

urlpatterns = [
    path('register', Create_User_View, name = 'registration_page'),
    path('login', User_Login_View, name = 'user_login'),
    path('logout', User_Logout_View, name = 'logout'),
    path('create', create_blog_post_view, name = 'create_blog_post'),
    path('all_blogs', view_all_blogs, name = 'view_my_blogs'),
    path('dashboard', Dashboard_View, name = 'dashboard'),
    path('delete_post/<str:title>/<str:author>', delete_post_view, name = 'delete'),
    path('update_post/<str:title>/<str:author>', update_certain_blog_view, name = 'update'),
    path('subscribe', subscribe_to_new_user_view, name = 'subscribe'),
    path('admin/', admin.site.urls),
]
