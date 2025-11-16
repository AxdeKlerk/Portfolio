from django.shortcuts import render, get_object_or_404, redirect
from .models import About, Blog, Project, CV
from django.http import FileResponse, Http404
import mimetypes
import os
from django.core.mail import send_mail
from django.contrib import messages


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
    if request.method == "POST":
        first = request.POST.get("first_name")
        last = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        full_message = f"""
        New message from your portfolio contact form:

        Name: {first} {last}
        Email: {email}
        Phone: {phone}

        Message:
        {message}
                """

        send_mail(
            subject="New Portfolio Contact Form Submission",
            message=full_message,
            from_email="axdeklerk@gmail.com",   # your email
            recipient_list=["axdeklerk@gmail.com"],  # where it should arrive
        )

        # For now: just show a success message  
        messages.success(request, "Thank you — your message has been sent! I will reply as soon as humanly possible.")

        return redirect("portfolio:contact")

    return render(request, "portfolio/contact.html", {"page": "contact"})
