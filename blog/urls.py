from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.PostList.as_view(), name='post_list'),
    url(r'^page/(?P<pn>[0-9]+)/$', views.PostList.as_view(), name='post_page_list'),

    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/best/$', views.best_posts, name="best"),
    url(r'^post/popular/$', views.popular, name="popular"),
    url(r'^post/plus/(?P<pk>[0-9]+)/$', views.plus, name='plus'),
    url(r'^post/minus/(?P<pk>[0-9]+)/$', views.minus, name='minus'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
]