from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^$', 'maptoolapp.views.index', name='index'),
    url(r'^lti_launch$', 'maptoolapp.views.lti_launch', name='lti_launch'),
    url(r'^main$', 'maptoolapp.views.main', name='main'),
    url(r'^table_view$', 'maptoolapp.views.table_view', name='table_view'),
    url(r'^user_edit_view$', 'maptoolapp.views.user_edit_view', name='user_edit_view'),
    url(r'^markers_class_xml$', 'maptoolapp.views.markers_class_xml', name='markers_class_xml'),
    url(r'^addoredituser$', 'maptoolapp.views.addoredituser', name='adduser'),
    url(r'^tool_config$', 'maptoolapp.views.tool_config', name='tool_config'),
)

