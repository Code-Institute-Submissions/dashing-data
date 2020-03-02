from django.urls import path, include
from .views import register, profile, logout, login
from . import urls_reset

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('login/', login, name='login'),
    path('password-reset/', include(urls_reset)),
]