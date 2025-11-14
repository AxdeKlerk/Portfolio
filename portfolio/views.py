from django.shortcuts import render, get_object_or_404
from .models import About, Blog, Project, CV


def home(request):
    return render(request, 'portfolio/home.html', {'page': 'home'})


def about(request):
    about = About.objects.first()
    return render(request, 'portfolio/about.html', {'page': 'about', 'about': about})


def projects(request):
    projects = Project.objects.all().order_by('-submission_date')
    return render(request, 'portfolio/projects.html', {'page': 'project', 'projects' : projects})


def blog_list(request):
    blogs = Blog.objects.all().order_by('-published_date')
    return render(request, 'portfolio/blog.html', {'page': 'blog', 'blogs': blogs })


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'portfolio/blog_detail.html', {'page': 'blog', 'blog': blog})


def cv(request):
    cv = CV.objects.first()
    return render(request, 'portfolio/cv.html', {'page': 'cv', 'cv': cv})


def contact(request):
    return render(request, 'portfolio/contact.html', {'page': contact})
