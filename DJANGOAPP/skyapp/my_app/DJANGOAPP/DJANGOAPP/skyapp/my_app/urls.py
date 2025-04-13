from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('aboutus.html', views.about, name='about'),
    path('contactus.html', views.contact, name='contact'),
    path('home.html', views.home, name='home')
]
