from django.views.generic.simple import redirect_to
from django.conf.urls import patterns, include, url

print 'URLS RULE'
urlpatterns = patterns('questions.views',
	url(r'^$', 'index'),
	url(r'^add/$', 'add_question'),
	url(r'^vote/(?P<id>\d+)/(?P<vote>\d+)/$', 'vote'),


)