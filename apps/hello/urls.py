from django.conf.urls import patterns, url


urlpatterns = patterns(
    'apps.hello.views',
    url(r'^$', 'main', name='main'),
)
