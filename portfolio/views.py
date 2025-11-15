from django.shortcuts import render, get_object_or_404
from .models import About, Blog, Project, CV
from django.http import FileResponse, Http404
import mimetypes
import os


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


def download_cv_pdf(request):
    cv = CV.objects.first()
    if not cv or not cv.pdf_cv_link:
        raise Http404("PDF not found")

    file_path = cv.pdf_cv_link.path
    filename = "Ax-de-Klerk-CV.pdf"

    return FileResponse(
        open(file_path, "rb"),
        content_type=mimetypes.guess_type(file_path)[0] or "application/pdf",
        as_attachment=True,
        filename=filename
    )


def download_cv_doc(request):
    cv = CV.objects.first()
    if not cv or not cv.doc_cv_link:
        raise Http404("DOC not found")

    file_path = cv.doc_cv_link.path
    filename = "Ax-de-Klerk-CV.docx"

    return FileResponse(
        open(file_path, "rb"),
        content_type=mimetypes.guess_type(file_path)[0] or "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        as_attachment=True,
        filename=filename
    )


def contact(request):
    return render(request, 'portfolio/contact.html', {'page': contact})
