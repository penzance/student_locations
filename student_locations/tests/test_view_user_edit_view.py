from unittest import TestCase
from mock import patch, ANY, DEFAULT, Mock, MagicMock
from django.test import RequestFactory
from django_auth_lti import const
from student_locations.views import user_edit_view

@patch.multiple('student_locations.views', render=DEFAULT)
class TestUserEditView(TestCase):
    longMessage = True

    def setUp(self):
        self.resource_link_id = '1234abcd'
        self.section_id = 5678
        self.sis_section_id = 8989
        self.request = RequestFactory().get('/fake-path')
        self.request.user = Mock(name='user_mock')
        self.request.user.is_authenticated.return_value = True
        self.request.session = {
            'LTI_LAUNCH': {
                'resource_link_id': self.resource_link_id,
                'roles': [const.INSTRUCTOR],
                'user_id' : 'user123'
            }
        }

    @patch('student_locations.views.getparamfromsession')
    def test_view_user_edit_no_resource_link_id(self, get_param_mock, render):
        """ test that the user_edit_view renders the error page 
            if getparamfromsession returns None """
        request = self.request
        request.session['LTI_LAUNCH']['resource_link_id'] = None
        get_param_mock.return_value = None
        user_edit_view(request)
        render.assert_called_with(request, 
        	'student_locations/error.html', ANY)

    @patch('student_locations.views.getparamfromsession')
    def test_view_user_edit_no_user_id(self, get_param_mock, render):
        """ test that the user_edit_view renders the error page 
            if getparamfromsession returns None """
        request = self.request
        get_param_mock.return_value = None
        user_edit_view(request)
        render.assert_called_with(request, 
            'student_locations/error.html', ANY)

    @patch('student_locations.views.StudentLocationForm')
    def test_view_user_edit_no_student(self, form_mock, render):
        """ test that the user_edit_view renders the error page 
            if getparamfromsession returns None """
        request = self.request
        Location = Mock(name='locations_mock')
        Location.objects.get.return_value = None 
        user_edit_view(request)
        form_mock.assert_called()



