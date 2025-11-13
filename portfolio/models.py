from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.text import slugify

class About(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    profile_image = CloudinaryField('image', blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=False)
    summary = models.TextField(max_length=800, blank=True, null=True)
    blog_image = CloudinaryField('image', blank=True, null=True)
    content = models.TextField(blank=False, null=False)
    author = models.CharField(max_length=100, default='Ax de Klerk')
    published_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Project(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    project_image = CloudinaryField('image', blank=True, null=True)
    description = models.TextField(blank=False, null=False)
    deployed_project_link = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    submission_date = models.DateTimeField(blank=False, null=False)

    def __str__(self):
        return self.title