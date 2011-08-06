from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('sso.views',
    url(r'^login/?', 'sso.views.login', name='login'),
    url(r'^validate/?', 'sso.views.validate', name='validate'),
)
