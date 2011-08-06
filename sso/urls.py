from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('sso.views',
    url(r'^cas/login/?', 'sso.views.login', name='login'),
    url(r'^cas/validate/?', 'sso.views.validate', name='validate'),
)
