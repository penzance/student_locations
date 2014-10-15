from unittest import TestCase
from mock import patch, ANY, DEFAULT, Mock, MagicMock
from django.test import RequestFactory
from django_auth_lti import const
from student_locations.views import index

@patch.multiple('student_locations.views', render=DEFAULT)
class TestIndexView(TestCase):
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


    def test_view_index(self, render):
        """ test that the index view renders the index page """
        request = self.request
        index(request)
        render.assert_called_with(request, 'student_locations/index.html')
