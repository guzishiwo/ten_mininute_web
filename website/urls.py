from django.conf.urls import url
from website.views import HomePageView, ArticleCommentView

urlpatterns = [
    url(
        regex=r'^$',
        view=HomePageView.as_view(),
        name='articles'
    ),
    url(
        regex=r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<title_slug>[-\w]+)',
        view=ArticleCommentView.as_view(),
        name='article_detail'
    )
]