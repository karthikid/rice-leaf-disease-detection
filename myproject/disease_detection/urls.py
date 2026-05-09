from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home, name='home'),
    path('detect/', views.detect, name='detect'),
    path('logout/', views.logout_view, name='logout'),
    path('result/', views.result, name='result'),
]