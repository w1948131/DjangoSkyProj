from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Employee
from .forms import AdminCreateUserForm
from django.contrib import messages

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('engineerdashboard')
        else:
            return render(request, 'my_app/home.html', {'error': 'invalid password or username'})
        
    return render(request, 'my_app/home.html')

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            if User.objects.filter(username=username).exists():
                return render(request, 'my_app/home.html', {'error': 'username already exists'})
            
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            login(request, user)
            
            return redirect('home')
        else:
            return render(request, 'my_app/home.html', {'error': 'Enter credentials in all fields'})
    return redirect('home')

def admin_create_view(request):
    if request.method == "POST":
         form = AdminCreateUserForm(request.POST)
         if form.is_valid():
            form.save()
            messages.success(request, 'New employee created successfully!')
            return redirect('adminpage')  
    else:
        form = AdminCreateUserForm()

    return render(request, 'my_app/adminpage.html', {'form': form})
    

def home(request):
    return render(request, "my_app/home.html")

def about(request):
    return render(request, "my_app/aboutus.html")

def contact(request):
    return render(request, "my_app/contactus.html")

def profile(request):
    return render(request, "my_app/profile.html")

def engineerdashboard(request):
    return render(request, "my_app/engineerdashboard.html")

def adminpage(request):
    return render(request, "my_app/adminpage.html")
