from django.db import models


class Video(models.Model):
    title = models.CharField(null=True, blank=True, max_length=300)
    content = models.TextField(null=True, blank=True)
    url_image = models.URLField(null=True, blank=True)
    editor_choice = models.BooleanField(default=False)

    def __str__(self):
        return self.title