from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from website.models.articles import Article, Comment
from django.contrib.auth.models import User
from website.models.user import UserProfile
from website.models.video import Video


class ArticleModelTest(TestCase):
    def create_article(self, title='first title', hits=300, content='test data'):
        return Article.objects.create(title=title, content=content, hits=hits)

    def expect_absoulte_url(self, slug_title):
        slash_time = datetime.now().strftime('%Y/%m/%d')
        return '/articles/{slash_time}/{slug_title}'.format(slash_time=slash_time, slug_title=slug_title)

    def test_article_creation(self):
        w = self.create_article()
        self.assertTrue(isinstance(w, Article))
        self.assertEqual(w.__str__(), w.title)

    def test_create_articles_by_desc(self):
        w = self.create_article()
        self.assertTrue(isinstance(w, Article))
        self.assertEqual(w.__str__(), w.title)
        w2 = self.create_article(title='two title', hits=400)
        self.assertTrue(isinstance(w2, Article))
        self.assertEqual(w2.__str__(), w2.title)

        saved_items = Article.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_save_article = saved_items[0]
        two_save_article = saved_items[1]

        # desc by hits fields
        self.assertEqual(first_save_article.title, 'two title')
        self.assertEqual(first_save_article.slug, 'two-title')
        self.assertEqual(first_save_article.content, 'test data')
        self.assertEqual(first_save_article.get_absolute_url(),
                         self.expect_absoulte_url(first_save_article.slug))
        self.assertEqual(first_save_article.hits, 400)

        self.assertEqual(two_save_article.title, 'first title')
        self.assertEqual(two_save_article.slug, 'first-title')
        self.assertEqual(two_save_article.get_absolute_url(),
                         self.expect_absoulte_url(two_save_article.slug))
        self.assertEqual(two_save_article.content, 'test data')
        self.assertEqual(two_save_article.hits, 300)


class CommentModelTest(TestCase):
    def create_article(self, title='first title', hits=300, content='test data'):
        return Article.objects.create(title=title, content=content, hits=hits)

    def create_comment(self, name='test', content='simple content'):
        return Comment(name=name, content=content, belong_to=self.create_article())

    def test_comment_creation(self):
        w = self.create_comment()
        self.assertTrue(isinstance(w, Comment))
        self.assertEqual(w.__str__(), w.name)


class VideoModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_superuser(
            'test_1', 'micro-test', 'ww'
        )
        self.user2 = User.objects.create_user(
            'test_2', 'micro-test2', 'ww'
        )
        self.user_profile_1 = UserProfile.objects.create(
            belong_to=self.user1, profile_image='img', last_activity=timezone.now(),

        )
        self.user_profile_2 = UserProfile.objects.create(
            belong_to=self.user2, profile_image='img', last_activity=timezone.now()
        )
        self.video = Video.objects.create(
            title='title', content='simple content'
        )

    def test_video_map_multi_user(self):
        video = self.video
        video.users.add(self.user_profile_1, self.user_profile_2)
        users = self.video.users.all()
        self.assertEqual(list(users), [self.user_profile_1, self.user_profile_2])

    # def test_filter_collected_user(self):
    #     video = self.video
    #     video.users.add(self.user_profile_1, self.user_profile_2)
    #     vid = Video.objects.filter(users__in=[])
    #     # if not vid:
