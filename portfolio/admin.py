from django.contrib import admin
from .models import About, Blog
from django.contrib.admin import register

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', 'profile_image', 'github_link', 'linkedin_link')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date')
    fields = ('title', 'summary', 'blog_image', 'content', 'author', 'published_date')
    readonly_fields = ('published_date',)