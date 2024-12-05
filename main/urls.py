from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'main'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^accounts/profile/$', views.profile, name='profile'),
    re_path(r'^accounts/profile/change_status/(?P<designs_id>\d+)/$', views.change_status, name='change_status'),
    re_path(r'^accounts/profile/delete/$', views.DeleteUserView.as_view(), name='profile_delete'),
    re_path(r'^accounts/profile/create_disign/$', views.create_design, name='create_disign'),
    re_path(r'^design/delete/(?P<design_id>\d+)/$', views.delete_design, name='delete_design'),
    re_path(r'^accounts/login/$', views.BBLoginView.as_view(), name='login'),
    re_path(r'^accounts/logout/$', views.BBLogoutView.as_view(), name='logout'),
    re_path(r'^accounts/register/$', views.RegisterUserView.as_view(), name='register'),
    re_path(r'^accounts/register/done/$', views.RegisterDoneView.as_view(), name='register_done'),
    re_path(r'^accounts/register/activate/(?P<sign>.+)/$', views.user_activate, name='register_activate'),
    re_path(r'^category/$', views.CategoryListView.as_view(), name='category'),
    re_path(r'^category/(?P<pk>\d+)$', views.CategoryDetailView.as_view(), name='category-detail'),
    re_path(r'^category/delete/(?P<category_id>\d+)/$', views.delete_category, name='delete_category'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)