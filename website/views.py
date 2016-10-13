from django.views import generic
from django.core.paginator import EmptyPage
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from website.forms import CommentForm
from website.models import Article, Video


class HomePageView(generic.ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'list_details.html'


class ArticleViewMixin(generic.TemplateView):
    model = Article
    template_name = 'article-detail.html'

    def get_object(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        day = self.kwargs.get("day")
        slug_title = self.kwargs.get("title_slug")
        return self.model.objects.filter(create_on__year=year,
                                         create_on__month=month,
                                         create_on__day=day).get(slug=slug_title)

    def get_context_data(self, **kwargs):
        context = super(ArticleViewMixin, self).get_context_data(**kwargs)
        context['article'] = self.get_object()
        return context


class ArticleCommentView(ArticleViewMixin, generic.FormView):
    form_class = CommentForm

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def form_valid(self, form):
        form.instance.belong_to = self.get_object()
        form.save(commit=True)
        return super(ArticleCommentView, self).form_valid(form)


def page_numbering(queryset, paginate_by, request_page):
    paginator = Paginator(queryset, paginate_by)
    try:
        pagination = paginator.page(request_page)
    except PageNotAnInteger:
        pagination = paginator.page(1)
    except EmptyPage:
        pagination = paginator.page(paginator.num_pages)

    index = pagination.number - 1
    limit = 5
    max_index = len(paginator.page_range)
    start_index = index - limit if index >= limit else 0
    end_index = index + limit if index <= max_index - limit else max_index

    page_range = list(paginator.page_range)[start_index:end_index]
    return pagination, page_range


class VideoView(generic.ListView):
    model = Video
    template_name = 'listing.html'
    paginate_by = 9
    queryset = Video.objects.all()

    def get_context_data(self, **kwargs):
        context = super(VideoView, self).get_context_data(**kwargs)
        page = self.request.GET.get('page', '1')
        context['vids_list'], context['page_range'] = page_numbering(self.queryset, self.paginate_by, page)
        return context