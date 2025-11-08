from django.shortcuts import render
from .models import About

def about(request):
    about = About.objects.first()
    return render(request, 'portfolio/about.html', {'about': about})


