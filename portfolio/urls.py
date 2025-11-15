from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('blog/', views.blog_list, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('cv/', views.cv, name='cv'),
    path("cv/download/pdf/", views.download_cv_pdf, name="download_cv_pdf"),
    path("cv/download/doc/", views.download_cv_doc, name="download_cv_doc"),
    path('contact/', views.contact, name='contact'),
]
