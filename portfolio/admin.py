from django.contrib import admin
from .models import About

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', 'profile_image', 'github_link', 'linkedin_link')


