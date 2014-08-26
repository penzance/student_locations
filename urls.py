from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'^$', 'student_locations.views.index', name='index'),
    url(r'^lti_launch$', 'student_locations.views.lti_launch', name='lti_launch'),
    url(r'^main$', 'student_locations.views.main', name='main'),
    url(r'^table_view$', 'student_locations.views.table_view', name='table_view'),
    url(r'^user_edit_view$', 'student_locations.views.user_edit_view', name='user_edit_view'),
    url(r'^markers_class_xml$', 'student_locations.views.markers_class_xml', name='markers_class_xml'),
    url(r'^addoredituser$', 'student_locations.views.addoredituser', name='adduser'),
    url(r'^tool_config$', 'student_locations.views.tool_config', name='tool_config'),
)

