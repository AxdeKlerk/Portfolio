from django.shortcuts import render
from .models import About, Blog

def home(request):
    return render(request, 'portfolio/home.html', {'page': 'home'})

def about(request):
    about = About.objects.first()
    return render(request, 'portfolio/about.html', {'page': 'about', 'about': about})

def projects(request):
    return render(request, 'portfolio/projects.html', {'page': 'projects'})

def blog_list(request):
    blogs = Blog.objects.all().order_by('-published_date')
    return render(request, 'portfolio/blog.html', {'page': 'blog', 'blogs': blogs })

def cv(request):
    return render(request, 'portfolio/cv.html', {'page': 'cv'})

def contact(request):
    return render(request, 'portfolio/contact.html', {'page': 'contact'})
