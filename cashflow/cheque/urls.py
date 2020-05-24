"""project_minsk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_process, name='logout'),
    path('make_cheque/', views.make_cheque, name='make_cheque'),
    path('activate_cheque/', views.activate_cheque, name='activate_cheque'),
    path('activate_cheque_process/', views.activate_cheque_process, name='activate_cheque_process'),
    path('show_cheque/<int:cheque_id>/', views.show_cheque, name='show_cheque'),
    path('login/', views.login_page, name='login_page'),
    path('login_process/', views.login_process, name='login_process'),
    path('process_cheque/', views.process_cheque, name='process_cheque'),
    path('history/', views.history, name='history'),
    path('user/<int:user_id>/', views.user_view, name='user_view',)
]
