from django.urls import path
from .views import test, login_view, register_view, logout_view

urlpatterns = [
    path('', test, name='test'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register')
]