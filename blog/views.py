from django.views.generic import View
from django.shortcuts import render, redirect
from blog.models import Article, Comment
from blog.forms import CommentForm


def home_page(request):
    if request.method == 'GET':
        Article.objects.create(title='test_one', content='test content', hits=300)
        Article.objects.create(title='test_two', content='desc content', hits=400)
        articles = Article.objects.all()
        return render(request, 'detail.html', {'article_list': articles})


def detail_page(request):
    if request.method == "GET":
        form = CommentForm
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            content = form.cleaned_data['content']
            c = Comment.objects.create(name=name, content=content)
            return redirect(to='detail')
    context = {}
    comment_list = Comment.objects.all()
    context['comment_list'] = comment_list
    context['form'] = form
    return render(request, 'article-detail.html', context)
