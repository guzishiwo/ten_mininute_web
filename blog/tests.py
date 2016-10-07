from unittest import skip
from django.test import TestCase
from django.http import HttpRequest
from django.core.urlresolvers import resolve, reverse
from django.template.loader import render_to_string
from blog.forms import CommentForm
from blog.views import HomePageView, CommentFormView
from blog.models import Article, Comment


class ArticleModelTest(TestCase):

    def create_article(self, title='first title', hits=300, content='test data'):
        return Article.objects.create(title=title, content=content, hits=hits)

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
        self.assertEqual(first_save_article.content, 'test data')
        self.assertEqual(first_save_article.hits, 400)

        self.assertEqual(two_save_article.title, 'first title')
        self.assertEqual(two_save_article.content, 'test data')
        self.assertEqual(two_save_article.hits, 300)


class CommentModelTest(TestCase):

    def create_comment(self, name='test', content='simple content'):
        return Comment.objects.create(name=name, content=content)

    def test_comment_creation(self):
        w = self.create_comment()
        self.assertTrue(isinstance(w, Comment))
        self.assertEqual(w.__str__(), w.name)


class CommentFormTest(TestCase):

    def test_comment_form(self):
        form = CommentForm()
        self.assertIn('placeholder="Enter your content"', form.as_p())

    def test_comment_form_validation_for_valid_name(self):
        form = CommentForm(data={'name': 'test', 'content': 'simple content', 'create_on': 'xxxxx'})
        self.assertTrue(form.is_valid())
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

    def test_detail_url_resolve_to_detail_page_view(self):
        view = resolve('/detail')
        self.assertEqual(view.func.__name__,
                         CommentFormView.as_view().__name__)

    def test_detail_page_renders_detail_template(self):
        response = self.client.get('/detail')
        self.assertTemplateUsed(response, 'article-detail.html')

    # def test_detail_page_use_item_form(self):
    #     response = self.client.get('/detail')
    #     # self.assertEqual(response.context['comment_list'], CommentForm)
    #     self.assertMultiLineEqual(response.context['comment_list'], CommentForm)


class NewCommentTest(TestCase):

    def test_normal_comment_sent_back_to_detail_template(self):
        comment_data = {'name': 'first', 'content': 'content'}
        rsp = self.client.post('/detail', data=comment_data)
        self.assertEqual(rsp.status_code, 302)
        response = self.client.get(rsp.url)
        self.assertTemplateUsed(response, 'article-detail.html')
        self.assertEqual(Comment.objects.get(name='first').name,
                         'first')


class HomePageTest(TestCase):

    def test_root_url_resolve_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func.__name__, HomePageView.as_view().__name__)

    def test_visit_home_page(self):
        response = self.client.get('/')
        self.assertIn('ten minutes', response.content.decode())

    def test_visit_home_page_template(self):
        article = Article.objects.create(title='12345', content='haha', hits=300)
        response = self.client.get('/')
        self.assertIn('12345', response.content.decode())
        self.assertIn('haha', response.content.decode())
        self.assertIn('300', response.content.decode())





