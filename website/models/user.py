from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    belong_to = models.OneToOneField(to=User, related_name='profile')
    profile_image = models.FileField(upload_to='profile_image')
    last_activity = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=10, default='man')
    nickname = models.CharField(max_length=128, null=True)
    phone = models.IntegerField(null=True)
    github = models.EmailField(null=True)

    def __str__(self):
        return self.nickname

    # def save(self, *args, **kwargs):
    #     self.nickname = 'ten_minute' + self.belong_to.username
    #     super(UserProfile, self).save(*args, **kwargs)