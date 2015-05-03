from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
    url(r'^$', views.user_login, name='user_login'),
    url(r'^index/$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^user/(?P<username_url>\w+)$', views.editUser, name='username'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/(?P<username_url>\w+)/$', views.register, name='register'),
    url(r'^delete/(?P<username_url>\w+)/$', views.deleteUser, name='delete'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^todo/$', views.todo, name='todo'),
    )
