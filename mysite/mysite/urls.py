from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^FindTeammates/', include('FindTeammates.urls',namespace="FindTeammates")),
    url('', include('django.contrib.auth.urls', namespace='auth')),
)
