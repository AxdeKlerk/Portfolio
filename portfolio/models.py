from django.db import models
from cloudinary.models import CloudinaryField

class About(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=1000)
    bio = models.TextField()
    profile_image = CloudinaryField('image', blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name