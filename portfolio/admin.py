from django.contrib import admin
from .models import About, Blog, Project, CV
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


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'submission_date')
    fields = ('title', 'project_image', 'description', 'tools_used', 'grade_received', 'deployed_project_link', 'github_link', 'submission_date')


@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ('pdf_cv_link', 'doc_cv_link')
    fields = ('cv_image_page_1', 'cv_image_page_2', 'pdf_cv_link', 'doc_cv_link')
