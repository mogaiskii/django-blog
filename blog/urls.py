from django.conf.urls import url
from . import views


urlpatterns = [
    # post lists
    url(r'^$', views.PostList.as_view(), name='post_list'),
    url(r'^page/(?P<pn>[0-9]+)/$', views.PostList.as_view(), name='post_page_list'),
    url(r'^post/best/$', views.best_posts, name="best"),
    url(r'^post/popular/$', views.popular, name="popular"),


    # post detail
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),


    # post edit/create
    url(r'^post/new/$', views.post_edit, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),


    ## ajax requests
    # rate
    url(r'^post/rate/(?P<pk>[0-9]+)/(?P<change>\w+)$', views.rate),
    # comment
    url(r'^post/(?P<pk>\d+)/comment/$', views.comment_create, name='add_comment_to_post'),


    ## blogs system
    url(r'^blog/(?P<pk>[0-9]+)/$', views.blog_detail),


    # registration override
    url(r'^accounts/register/$', views.RegisterFormView.as_view(), name="registration"),

]