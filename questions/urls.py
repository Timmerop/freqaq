from django.views.generic.simple import redirect_to
from django.conf.urls import patterns, include, url

urlpatterns = patterns('questions.views',
	url(r'^$', 'index'),
	url(r'^add/$', 'add_question'),
	url(r'^vote/(?P<id>\d+)/(?P<vote>\w+)/$', 'vote'),
)