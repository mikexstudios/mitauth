from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('sso.views',
    url(r'^login/?', 'login', name='login'),
    url(r'^validate/?', 'validate', name='validate'),
)
