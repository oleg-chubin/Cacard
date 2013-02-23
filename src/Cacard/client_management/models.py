from django.db import models

# Create your models here.

class Client(models.Model):
    slug = models.CharField(max_length=25)