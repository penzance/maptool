from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^$', 'maptoolapp.views.index', name='index'),
    url(r'^lti_launch$', 'maptoolapp.views.lti_launch', name='lti_launch'),
    url(r'^main$', 'maptoolapp.views.main', name='main'),
    url(r'^table_view$', 'maptoolapp.views.table_view', name='table_view'),
    url(r'^markers_class_xml$', 'maptoolapp.views.markers_class_xml', name='markers_class_xml'),
    url(r'^addoreditlocation$', 'maptoolapp.views.addoreditlocation', name='addlocation'),
    url(r'^tool_config$', 'maptoolapp.views.tool_config', name='tool_config'),
    url(r'^add_location$', 'maptoolapp.views.add_location', name='add_location'),
    url(r'^toolinstanceconfig$', 'maptoolapp.views.toolinstanceconfig', name='toolinstanceconfig'),
    url(r'^deleteview$', 'maptoolapp.views.deleteview', name='deleteview'),
    url(r'^displaymaps$', 'maptoolapp.views.displaymaps', name='displaymaps'),
    url(r'^mapsview$', 'maptoolapp.views.mapsview', name='mapsview'),
    )

