from django.contrib import admin

from website.models.articles import Article, Comment
from website.models.user import UserProfile
from website.models.video import Video, Ticket

# Register your models here.
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Video)
admin.site.register(Ticket)
