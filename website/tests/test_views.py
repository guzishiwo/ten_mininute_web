from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve, reverse
from website.models.articles import Article, Comment
from website.models.user import UserProfile
from website.models.video import Video, Ticket
from website.forms import CommentForm
from website.views import HomePageView, ArticleCommentView


class DetailPageTest(TestCase):

    def setUp(self):
        self.article_one = Article.objects.create(title='first title', content='simple content', hits=300)
        self.comment_one = Comment.objects.create(name='aly', content='test comment', belong_to=self.article_one)
        self.article_url = self.article_one.get_absolute_url()

    def test_detail_url_resolve_to_detail_page_view(self):
        view = resolve(self.article_one.get_absolute_url())
        self.assertEqual(view.func.__name__,
                         ArticleCommentView.as_view().__name__)

    def test_article_detail_page_renders_detail_template(self):
        response = self.client.get(self.article_url)
        self.assertTemplateUsed(response, 'articles/article-detail.html')

    def test_article_detail_page_use_item_form(self):
        response = self.client.get(self.article_url)
        self.assertEqual(response.context['article'], self.article_one)

    # def test_comment_form_success(self):
    #     page = self.client.get(self.article_one.get_absolute_url())
    #     page.form['name'] = "Phillip"
        # page.form['content'] = "Simple Content"
        # page = page.form.submit()
        # self.assertRedirects(page, self.article_one.get_absolute_url())


class HomePageTest(TestCase):

    def test_root_url_resolve_to_home_page_view(self):
        found = resolve(reverse('articles'))
        self.assertEqual(found.func.__name__, HomePageView.as_view().__name__)

    def test_visit_home_page(self):
        response = self.client.get(reverse('articles'))
        self.assertIn('ten minutes', response.content.decode())

    def test_visit_home_page_template(self):
        article = Article.objects.create(title='first article', content='simple content', hits=300)
        response = self.client.get(reverse('articles'))
        self.assertIn('first article', response.content.decode())
        self.assertIn('simple content', response.content.decode())
        self.assertIn('300', response.content.decode())


class VideoDetailTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_superuser(
            'test_1', 'micro-test', 'ww'
        )
        self.user_profile_1 = UserProfile.objects.create(
            belong_to=self.user1, profile_image='img', last_activity=timezone.now(),

        )
        self.video = Video.objects.create(
            title='title', content='simple content'
        )
        self.ticket = Ticket.objects.create(
            voter=self.user_profile_1, video=self.video, choice='like'
        )

    def test_video_detail(self):
        user_login = self.client.login(username='test_1', password='ww')
        self.assertTrue(user_login)

        response = self.client.get(reverse('detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail.html')
