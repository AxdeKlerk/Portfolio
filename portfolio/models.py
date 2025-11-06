from django.db import models
from cloudinary.models import CloudinaryField

class About(models.Model):
    name = models.CharField(max_length=100)
    short_bio = models.CharField(max_length=250)
    description = models.TextField()
    profile_image = CloudinaryField('image', blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name