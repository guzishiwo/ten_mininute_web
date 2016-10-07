from django.views import generic
from django.core.urlresolvers import reverse_lazy
from blog.forms import CommentForm
from blog.models import Article, Comment


class HomePageView(generic.ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'detail.html'


class CommentFormView(generic.FormView):
    model = Comment
    template_name = 'article-detail.html'
    form_class = CommentForm
    success_url = reverse_lazy("detail")

    def get_context_data(self, **kwargs):
        context = super(CommentFormView, self).get_context_data(**kwargs)
        context['comment_list'] = self.model.objects.all()
        return context

    def form_valid(self, form):
        form.save(commit=True)
        return super(CommentFormView, self).form_valid(form)

