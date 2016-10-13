from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    belong_to = models.OneToOneField(to=User, related_name='profile')
    profile_image = models.FileField(upload_to='profile_image')
    last_activity = models.DateTimeField(null=True, blank=True)