from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from . import views

app_name = 'custom_admin'
urlpatterns = [
path('', views.index, name='index'),
path('login/',views.login, name = 'login'),
#path('register/',views.register, name = 'register'),
path('logout/',views.logoutUser, name = 'logout'),

# user management
path('users/', views.UserList, name='UserList'),
path('users/user_add', views.UserAdd, name='UserAdd'),
path('users/user_update/<int:id>', views.UserUpdate, name='UserUpdate'),
path('users/user_delete/<int:id>', views.UserDelete, name='UserDelete'),
path('users/user_change', views.UserChange, name='UserChange'),
path('users/user_change_psw', views.UserChangePsw, name='UserChangePsw'),
]
