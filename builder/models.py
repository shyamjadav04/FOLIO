from django.db import models
from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=100)
    skills = models.TextField()
    education = models.TextField(null=True, blank=True)
    projects = models.TextField()
    experience = models.TextField()
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    template = models.CharField(max_length=50)


    def __str__(self):
        return self.name
# Create your models here.
