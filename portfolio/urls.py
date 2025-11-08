from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('about/', views.about, name='about'),
]
