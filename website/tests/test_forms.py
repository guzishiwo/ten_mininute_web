from datetime import datetime

from django.core.urlresolvers import resolve, reverse
from django.test import TestCase

from website.forms import CommentForm
from website.models.articles import Article, Comment
from website.models.video import Video
from website.views import HomePageView, ArticleCommentView

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