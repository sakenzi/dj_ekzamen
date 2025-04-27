from django.urls import path
from .views import user_register_view, user_login_view, user_logout_view, home_view


urlpatterns = [
    path('', home_view, name='home'),
    path('register', user_register_view, name='register'),
    path('login', user_login_view, name='login'),
    path('logout', user_logout_view, name='logout'),
]