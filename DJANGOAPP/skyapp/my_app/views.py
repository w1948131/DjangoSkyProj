from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, "my_app/home.html")

def about(request):
    return render(request, "my_app/aboutus.html")

def contact(request):
    return render(request, "my_app/contactus.html")
