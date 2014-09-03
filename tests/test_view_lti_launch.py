from unittest import TestCase
from mock import patch, ANY, DEFAULT, Mock
from django.test import RequestFactory
from django_auth_lti import const
from student_locations.views import lti_launch

@patch.multiple('student_locations.views', render=DEFAULT)
class TestLtiLaunchView(TestCase):
    longMessage = True

    def setUp(self):
        self.resource_link_id = '1234abcd'
        self.section_id = 5678
        self.sis_section_id = 8989
        self.request = RequestFactory().post('/fake-path')
        self.request.user = Mock(name='user_mock')
        self.request.user.is_authenticated.return_value = True
        self.request.session = {
            'LTI_LAUNCH': {
                'resource_link_id': self.resource_link_id,
                'roles': [const.INSTRUCTOR],
                'user_id' : 'user123'
            }
        }


    @patch('student_locations.views.redirect')
    def test_view_lti_launch_success(self, redirect_mock, render):
        """ test that the lti_launch view renders the main view on success """
        request = self.request
        lti_launch(request)
        redirect_mock.assert_called_with('sl:main')


    @patch('student_locations.views.validaterequiredltiparams')
    def test_view_lti_launch_user_not_authenticated(self, valid_lti_params_mock, render):
        """ test that the lti_launch view renders the error page if the required
            LTI params are not present in the session """
        request = self.request
        valid_lti_params_mock.return_value = False
        lti_launch(request)
        render.assert_called_with(request, 'student_locations/error.html', ANY)

