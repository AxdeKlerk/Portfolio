from django.db import models
from cloudinary.models import CloudinaryField

class About(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    profile_image = CloudinaryField('image', blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    summary = models.CharField(max_length=500, blank=True, null=True)
    blog_image = CloudinaryField('image', blank=True, null=True)
    content = models.TextField()
    author = models.CharField(max_length=100, default='Admin')
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title