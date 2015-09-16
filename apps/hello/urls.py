from django.conf.urls import patterns, url


urlpatterns = patterns(
    'apps.hello.views',
    url(r'^$', 'main', name='main'),
    url(r'^requests/$', 'http_requests', name='requests'),
    url(r'^edit/$', 'edit', name='edit'),
)
