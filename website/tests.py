from datetime import datetime
from django.test import TestCase
from django.http import HttpRequest
from django.core.urlresolvers import resolve, reverse
from django.template.loader import render_to_string
from website.forms import CommentForm
from website.views import HomePageView, ArticleCommentView
from website.models import Article, Comment


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


class CommentFormTest(TestCase):

    def create_article(self, title='first title', hits=300, content='test data'):
        return Article.objects.create(title=title, content=content, hits=hits)

    def test_comment_form(self):
        form = CommentForm()
        self.assertIn('placeholder="填写你的评论"', form.as_p())

    def test_comment_form_validation_for_valid_name(self):
        form = CommentForm(data={'name': 'test', 'content': 'simple content'})
        self.assertTrue(form.is_valid())
        form.instance.belong_to = self.create_article()
        comment = form.save()
        self.assertEqual(comment.name, "test")
        self.assertEqual(comment.content, "simple content")

    def test_comment_form_validation_for_invalid_name(self):
        form = CommentForm(data={'name': 'admin', 'content': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['name'],
            ["Your comment contains invalid words,please check it again."]
        )


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
        self.assertTemplateUsed(response, 'article-detail.html')

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





