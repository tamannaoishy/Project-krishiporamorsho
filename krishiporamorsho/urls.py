"""krishiporamorsho URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from problems.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('login', user_login, name='login'),
    path('admin_login', admin_login, name='admin_login'),
    path('signup', signup1, name='signup'),
    path('', index, name='index'),
    path('admin_home', admin_home, name='admin_home'),
    path('logout', Logout, name='logout'),
    path('profile', profile, name='profile'),
    path('changepassword', changepassword, name='changepassword'),
    path('upload_problems', upload_problems, name='upload_problems'),
    path('view_myproblems', view_myproblems, name='view_myproblems'),
    
    path('view_users', view_users, name='view_users'),
    path('all_problems', all_problems, name = 'all_problems'),
    path('solution/<int:pk>', solution, name = 'solution'),
    path('solved_problems', solved_problems, name = 'solved_problems'),
    path('admin_problems', admin_problems, name = 'admin_problems'),
    path('accepted_problems', accepted_problems, name = 'accepted_problems'),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  #whenever upload a file
