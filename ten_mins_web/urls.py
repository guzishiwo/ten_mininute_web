"""ten_mins_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import os
from django.conf.urls.static import static
from ten_mins_web.settings import BASE_DIR
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from website.views import VideoView
from website.views import VideoDetailView
from website.views import LoginView
from website.views import LogoutView
from website.views import RegisterView
from website.views import ChangePasswordView
from website.views import ChangeUserInfoView
from website.views import CollectVideoView

urlpatterns = [
    url(
        regex=r'^$',
        view=VideoView.as_view(),
        name='index'
    ),
    url(
        regex=r'^login',
        view=LoginView.as_view(),
        name='login'
    ),
    url(
        regex=r'^register',
        view=RegisterView.as_view(),
        name='register'

    ),
    url(
        regex=r'^logout',
        view=LogoutView.as_view(),
        name='logout'

    ),
    url(
        regex=r'^change_password/$',
        view=ChangePasswordView.as_view(),
        name='change_password'
    ),
    url(
        regex=r'^change_person_info/$',
        view=ChangeUserInfoView.as_view(),
        name="change_person_info"
    ),
    url(
        regex=r'^collect_videos/$',
        view=CollectVideoView.as_view(),
        name="collect_videos"
    ),
    url(
        regex=r'^detail/(?P<id>\d+)$',
        view=VideoDetailView.as_view(),
        name='detail'
    ),
    url(r'^admin/', admin.site.urls),
    url(r'^articles/', include('website.urls')),

]
urlpatterns += static('/upload/', document_root=os.path.join(BASE_DIR, 'upload'))
