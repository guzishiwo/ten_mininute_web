from faker import Factory
from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify


class Article(models.Model):
    title = models.CharField(blank=True, max_length=128, verbose_name='标题')
    content = models.TextField(null=True, blank=True, verbose_name='内容')
    slug = models.CharField(blank=True, max_length=128, unique=True)
    create_on = models.DateField(blank=True, auto_now_add=True, verbose_name='创建时间')
    update_on = models.DateField(auto_now=True, verbose_name='更新时间')
    hits = models.IntegerField(verbose_name='点击量')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        slash_time = str(self.create_on).split('-')
        return reverse(
            viewname='article_detail',
            kwargs={
                'year': slash_time[0],
                'month': slash_time[1],
                'day': slash_time[2],
                'title_slug': self.slug
            }
        )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-hits', 'create_on']


class Comment(models.Model):
    name = models.CharField(blank=True, max_length=50, verbose_name='昵称')
    content = models.TextField(max_length=500, verbose_name='评论')
    create_on = models.DateTimeField(auto_now_add=True)
    belong_to = models.ForeignKey(to=Article, related_name='under_comments')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['create_on']


class Video(models.Model):
    title = models.CharField(null=True, blank=True, max_length=300)
    content = models.TextField(null=True, blank=True)
    url_image = models.URLField(null=True, blank=True)
    editor_choice = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# f = open('img_urls.txt', 'r')
# fake = Factory.create()
# for url in f.readlines():
#     v = Video.objects.create(
#         title=fake.text(max_nb_chars=80),
#         content=fake.text(max_nb_chars=3000),
#         url_image=url,
#         editor_choice=fake.pybool()
#     )
#
#