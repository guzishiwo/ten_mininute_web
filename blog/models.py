from django.db import models

# Create your models here.


class Article(models.Model):
    title = models.CharField(null=True, blank=True, max_length=128, )
    content = models.CharField(null=True, blank=True, max_length=128)
    create_on = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    hits = models.IntegerField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-hits', 'create_on']


class Comment(models.Model):
    name = models.CharField(null=True, blank=True, max_length=50, verbose_name='昵称')
    content = models.TextField(max_length=500, blank=True, verbose_name='内容')
    create_on = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['create_on']