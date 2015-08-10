from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'maptool.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^lti_tools/basic_lti_app/', include('basic_lti_app.urls', namespace="basic_lti_app")),
    url(r'^lti_tools/maptoolapp/', include('maptoolapp.urls', namespace="maptoolapp")),
    url(r'^lti_tools/maps/', include('maps.urls', namespace="maps")),
    url(r'^lti_tools/auth_error/', 'maptool.views.lti_auth_error', name='lti_auth_error'),
)
