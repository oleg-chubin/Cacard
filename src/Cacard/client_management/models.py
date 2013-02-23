from django.db import models
from .utils import create_client_infrastructure
# Create your models here.

class Client(models.Model):
    slug = models.CharField(max_length=25)