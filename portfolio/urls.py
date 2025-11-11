from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('blog/', views.blog_list, name='blog'),
    path('cv/', views.cv, name='cv'),
    path('contact/', views.contact, name='contact'),
]
