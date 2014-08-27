from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.http import require_http_methods
from ims_lti_py.tool_config import ToolConfig
from django.conf import settings
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from student_locations.forms import StudentLocationForm
from student_locations.models import Locations
from student_locations.utils import validaterequiredltiparams, getparamfromsession

import logging 


logger = logging.getLogger(__name__)

@login_required()
@require_http_methods(['GET'])
def index(request):
    """
    Show the index file
    """
    return render(request, 'student_locations/index.html')

@login_required()
@require_http_methods(['POST'])
def lti_launch(request):
    """
    This method is here to build the LTI_LAUNCH dictionary containing all
    the LTI parameters and place it into the session. This is nessesary as we 
    need to access these parameters throughout the application and they are only 
    available the first time the application loads.
    """
    if request.user.is_authenticated():
        if validaterequiredltiparams(request):
            return redirect('sl:main')
        else: 
            return render(request, 'student_locations/error.html', {'message': 'Error: The LTI parameter lis_course_offering_sourcedid is required by this LTI tool.'})
    else:
        return render(request, 'student_locations/error.html', {'message': 'Error: user is not authenticated!'})

@login_required()
@require_http_methods(['GET'])
def main(request):
    """
    The main method dipslay the default view which is the map_view.
    """
    key = settings.STUDENT_LOCATIONS_TOOL.get('google_map_api_v3_key')
    return render(request, 'student_locations/map_view.html', {'request': request, 'api_key': key})


@login_required()
@require_http_methods(['GET'])
def user_edit_view(request):
    """
    Displays the user edit view which allows users to enter their contact
    and Location data for display on the google map.
    """
    course_id = getparamfromsession(request, 'lis_course_offering_sourcedid')
    user_id = getparamfromsession(request, 'user_id')
    if not course_id or not user_id:
        return render(request, 'student_locations/error.html', {'message': 'Unable to retrieve params from session. You might want to try reloading the tool.'})
   
    try:
        student = Locations.objects.get(course_id=course_id, user_id=user_id)
    except Locations.DoesNotExist:
        student = None

    if student:
        form = StudentLocationForm(instance=student)
    else:
        form = StudentLocationForm()

    return render(request, 'student_locations/user_edit_view.html', {'request': request, 'form': form})

@login_required()
def addoredituser(request):
    """
    The action method for the user_edit_view form.
    """
    course_id = getparamfromsession(request, 'lis_course_offering_sourcedid')
    user_id = getparamfromsession(request, 'user_id')
    
    try:
        student = Locations.objects.get(course_id=course_id, user_id=user_id)
    except Locations.DoesNotExist:
        student = None

    if student:
        form = StudentLocationForm(instance=student, user_id=user_id, course_id=course_id, data=request.POST)
    else:
        logger.debug('student is None')
        form = StudentLocationForm(user_id=user_id, course_id=course_id, data=request.POST)

    if form.is_valid():
        theform = form.save(commit=False)
        theform.user_id = user_id
        theform.course_id = course_id
        theform.save()
        key = settings.STUDENT_LOCATIONS_TOOL.get('google_map_api_v3_key')
        return render(request, 'student_locations/map_view.html', {'request': request, 'api_key' : key})
    else:
        return render(request, 'student_locations/user_edit_view.html', {'request': request, 'form': form})

@login_required()
@require_http_methods(['GET'])
def table_view(request):
    """
    renders the data and display of the table view of students
    """
    course_id = getparamfromsession(request, 'lis_course_offering_sourcedid')
    user_id = getparamfromsession(request, 'user_id')
    return render(request, 'student_locations/table_view.html', {'request': request, 'data' : students})

@login_required()
@require_http_methods(['GET'])
def markers_class_xml(request):
    """
    reders the XML containing the location data for the google map
    """
    course_id = getparamfromsession(request, 'lis_course_offering_sourcedid')
    students = Locations.objects.filter(course_id=course_id)
    return render_to_response('student_locations/markers.xml',
                          {'data' : students},
                          context_instance=RequestContext(request)) 

@require_http_methods(['GET'])
def tool_config(request):
    """
    This produces a Canvas specific XML config that can be used to
    add this tool to the Canvas LMS
    """
    if request.is_secure():
        host = 'https://' + request.get_host()
    else:
        host = 'http://' + request.get_host()

    url = host + reverse('sl:lti_launch')

    lti_tool_config = ToolConfig(
        title='Student Locations',
        launch_url=url,
        secure_launch_url=url,
    )
    account_nav_params = {
        'enabled': 'true',
        # optionally, supply a different URL for the link:
        # 'url': 'http://library.harvard.edu',
        'text': 'Student Locations',
    }
    lti_tool_config.set_ext_param('canvas.instructure.com', 'privacy_level', 'public')
    lti_tool_config.set_ext_param('canvas.instructure.com', 'course_navigation', account_nav_params)
    lti_tool_config.description = 'This LTI tool facilitates the display of Student Locations.'

    resp = HttpResponse(lti_tool_config.to_xml(), content_type='text/xml', status=200)
    return resp





