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
    path('login/', login_view, name="login"),
    path('register/', register_view, name='register'),
    path("", home_view, name="home"),
    path("admin/", admin.site.urls),
    
    ### public views ###
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("forum/<int:board_id>/", forum_view, name="forum"),
    path('forum/<int:board_id>/create-post/', create_post_view, name='post'),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", edit_profile_view, name="edit_profile"),
    path("create-profile/", create_profile_view, name="create_profile"),
    
    ### moderator views ###
    path('mod-control-panel/', board_control_view, name='board_control'),
    path('mod-control-panel/create-board/', create_board_view, name='create_board'),
    path('mod-control-panel/edit-board/<int:board_id>/', update_board_view, name='edit_board'),
    path('mod-control-panel/delete-board/<int:board_id>/', delete_board_view, name='delete_board'),
    path('mod-control-panel/delete-post/<int:post_id>/', delete_post_view, name='delete_post'),




]
