from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('aboutus.html', views.about, name='about'),
    path('contactus.html', views.contact, name='contact'),
    path('home.html', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('engineerdashboard/', views.engineerdashboard, name='engineerdashboard'),
    path('engineerdashboard.html', views.engineerdashboard, name='engineerdashboard'),
    path('profile.html', views.profile, name='profile'),
    path('adminpage/', views.admin_create_view, name='adminpage'),
    path('adminpage.html/contactus.html', views.contact, name='contact'),
    
]
