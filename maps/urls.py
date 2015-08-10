from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^$', 'maps.views.index', name='index'),
    url(r'^lti_launch$', 'maps.views.lti_launch', name='lti_launch'),
    url(r'^main$', 'maps.views.main', name='main'),
    url(r'^tool_config$', 'maps.views.tool_config', name='tool_config'),

    )

