from django.db import models
from .user import UserProfile
from django.core.urlresolvers import reverse


class Video(models.Model):
    title = models.CharField(null=True, blank=True, max_length=300)
    content = models.TextField(null=True, blank=True)
    url_image = models.URLField(null=True, blank=True)
    editor_choice = models.BooleanField(default=False)
    users = models.ManyToManyField(to='UserProfile', related_name='video')
    is_collected = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'id': self.id})


class Ticket(models.Model):
    voter = models.ForeignKey(to=UserProfile, related_name='voted_tickets')
    video = models.ForeignKey(to=Video, related_name='tickets')
    VOTE_CHOICES = (
        ('like', 'like'),
        ('dislike', 'dislike'),
        ('normal', 'normal'),
        )
    choice = models.CharField(choices=VOTE_CHOICES, max_length=10)

    def __str__(self):
        return str(self.id)
