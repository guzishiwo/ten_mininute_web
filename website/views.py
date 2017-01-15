from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views import generic
from django.shortcuts import render, redirect
from website.forms import LoginForm
from website.models.articles import Article
from website.models.user import UserProfile
from website.models.video import Video, Ticket
from website.forms import (
    CommentForm, UserCreateForm, ChangePasswordForm, ChangeUserInfoForm)
from rest_framework import serializers, viewsets, routers



class HomePageView(generic.ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'articles/list_details.html'


class ArticleViewMixin(generic.TemplateView):
    model = Article
    template_name = 'articles/article-detail.html'

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
    template_name = 'index.html'
    paginate_by = 9
    queryset = Video.objects.all()

    def get_context_data(self, **kwargs):
        context = super(VideoView, self).get_context_data(**kwargs)
        page = self.request.GET.get('page', '1')
        context['vids_list'], context['page_range'] = page_numbering(self.queryset, self.paginate_by, page)
        return context


class VideoDetailView(generic.View):
    model = Video
    template_name = 'detail.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = {}
        _id=self.kwargs['id']
        video_info = self.model.objects.get(id=_id)
        like_counts = Ticket.objects.filter(choice='like', video_id=_id).count()
        voter_id = self.request.user.profile.id
        try:
            user_ticket_for_this_video = Ticket.objects.get(voter_id=voter_id, video_id=_id)
            context['user_ticket'] = user_ticket_for_this_video
        except Exception as e:
            print('Video Detail View', e)
        context['like_counts'] = like_counts
        context['video_info'] = video_info
        context['user_profiles'] = self.model.objects.get(pk=_id).users.all()
        context['is_collected'] = video_info.is_collected
        print('user_profiles', context['user_profiles'])
        print('is_collected', context['is_collected'])
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        voter_id = self.request.user.profile.id
        _id = self.kwargs['id']
        collected = request.POST.get('collected')
        if 'vote' in request.POST:
            try:
                user_ticket_for_this_video = Ticket.objects.get(voter_id=voter_id, video_id=_id)
            except Ticket.DoesNotExist:
                Ticket.objects.create(voter_id=voter_id, video_id=self.kwargs['id'], choice=_id)
            else:
                user_ticket_for_this_video.choice = request.POST['vote']
                user_ticket_for_this_video.save()
        elif 'collected' in request.POST:
            video = self.model.objects.get(pk=_id)
            if collected == 'True':
                video.users.add(self.request.user.profile)
                video.is_collected = True
                video.save()
            else:
                video.users.remove(self.request.user.profile)
                video.is_collected = False
                video.save()
        else:
            print('Post unknown params')
        return redirect(to='detail', id=_id)


class LoginView(generic.FormView):
    template_name = 'user/Login.html'
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_active:
            return HttpResponseRedirect(reverse_lazy("index"))
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
        if user.is_active:
            login(self.request, user)
            messages.success(self.request, 'You are successfully logged in')
            return HttpResponseRedirect(reverse_lazy("index"))
        else:
            data = {'response': 'You are not allowed to this page'}
            return JsonResponse(data)


class RegisterView(generic.FormView):
    template_name = 'user/Register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('login')


class LogoutView(generic.RedirectView):
    url = 'login/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class ChangePasswordView(LoginRequiredMixin, generic.FormView):
    template_name = 'user/change_password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data.get("password"))
        user.save()
        user = authenticate(username=user.username, password=form.cleaned_data.get("password"))
        # login(self.request, user)
        return redirect(to='login')


class ChangeUserInfoView(generic.FormView):
    template_name = 'user/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy("change_person_info")

    def form_valid(self, form):
        form.instance.belong_to = self.request.user
        form.save()
        return super(ChangeUserInfoView, self).form_valid(form)


class CollectVideoView(generic.TemplateView):
    template_name = 'user/collect_videos.html'
    model = Video
    context_object_name = 'videos'

    def get_context_data(self, **kwargs):
        context = super(CollectVideoView, self).get_context_data(**kwargs)
        user_profile = self.request.user.profile
        context['videos'] = user_profile.video.all()
        return context


