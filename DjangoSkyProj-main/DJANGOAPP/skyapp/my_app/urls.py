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
    path('profile.html', views.profile, name='profile'),
    path('voting/', views.voting_view, name='voting'),
    path('summary/', views.summary, name='summary'),
    path('healthcard/', views.healthcard, name='healthcard'),
]
