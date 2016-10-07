from django.db import models

# Create your models here.


class Article(models.Model):
    title = models.CharField(blank=True, max_length=128, verbose_name='标题')
    content = models.TextField(null=True, blank=True, verbose_name='内容')
    create_on = models.DateTimeField(blank=True, auto_now_add=True, verbose_name='创建时间')
    update_on = models.DateField(auto_now=True, verbose_name='更新时间')
    hits = models.IntegerField(blank=True, verbose_name='点击量')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-hits', 'create_on']


class Comment(models.Model):
    name = models.CharField(blank=True, max_length=50, verbose_name='昵称')
    content = models.TextField(max_length=500, verbose_name='评论')
    create_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['create_on']