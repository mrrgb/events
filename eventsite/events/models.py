from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    owner = models.ForeignKey(User)
    description = models.CharField(max_length=1000)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=256)
