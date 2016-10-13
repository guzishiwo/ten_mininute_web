from django.contrib import admin
from website.models import Article, Comment, UserProfile
# Register your models here.
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(UserProfile)
