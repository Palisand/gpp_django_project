from django.conf.urls import patterns, url
from gpp import views

urlpatterns = patterns('',
   url(r'^$', views.index, name='index'),
   url(r'^results/$', views.results, name='results'),#query/$ ???
   # url(r'^results/sort/(?P<sort_method>\w+)/$', views.sort, name='sort')
   # url(r'^publication/(?P<pub_id>\cheatsheet for integer)')
)