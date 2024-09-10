from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=10, default='active')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return f' title: {self.title} '