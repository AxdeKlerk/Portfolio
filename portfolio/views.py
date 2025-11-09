from django.shortcuts import render
from .models import About

def home(request):
    return render(request, 'portfolio/home.html', {'page': 'home'})

def about(request):
    about = About.objects.first()
    return render(request, 'portfolio/about.html', {'page': 'about', 'about': about})

def projects(request):
    return render(request, 'portfolio/projects.html', {'page': 'projects'})

def blog(request):
    return render(request, 'portfolio/blog.html', {'page': 'blog'})

def cv(request):
    return render(request, 'portfolio/cv.html', {'page': 'cv'})

def contact(request):
    return render(request, 'portfolio/contact.html', {'page': 'contact'})
