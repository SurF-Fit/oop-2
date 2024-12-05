from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static
from setuptools.extern import names

from . import views

app_name = 'main'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^accounts/profile/$', views.profile, name='profile'),
    re_path(r'^accounts/profile/delete/$', views.DeleteUserView.as_view(), name='profile_delete'),
    re_path(r'^accounts/profile/create_disign/$', views.create_design, name='create_disign'),
    re_path(r'^design/delete/(?P<design_id>\d+)/$', views.delete_design, name='delete_design'),
    re_path(r'^accounts/login/$', views.BBLoginView.as_view(), name='login'),
    re_path(r'^accounts/logout/$', views.BBLogoutView.as_view(), name='logout'),
    re_path(r'^accounts/register/$', views.RegisterUserView.as_view(), name='register'),
    re_path(r'^accounts/register/done/$', views.RegisterDoneView.as_view(), name='register_done'),
    re_path(r'^accounts/register/activate/(?P<sign>.+)/$', views.user_activate, name='register_activate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)