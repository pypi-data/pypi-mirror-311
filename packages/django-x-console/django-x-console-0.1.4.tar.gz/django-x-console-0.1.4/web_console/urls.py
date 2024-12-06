from django.urls import path

from . import views

app_name = 'console'

urlpatterns = [
    path('', views.console_layout, name='console_layout'),

    path('login', views.console_login, name='console_login'),

    path('logout', views.console_logout, name='console_logout'),

    path('menu', views.console_menu, name='console_menu'),

    path('home', views.console_home, name='console_home'),
]
