from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.http import require_http_methods
from ims_lti_py.tool_provider import DjangoToolProvider
from ims_lti_py.tool_config import ToolConfig
from django.conf import settings
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from student_locations.forms import StudentLocationForm
from student_locations.models import Locations
import logging 

logger = logging.getLogger(__name__)

#@login_required()
@require_http_methods(['GET'])
def index(request):
    """
    Show the index file
    """
    logger.info("request to index.")
    return render(request, 'student_locations/index.html')

@login_required()
@require_http_methods(['POST'])
def lti_launch(request):
    """
    launch the lti application
    """	
    if request.user.is_authenticated():
    	key = settings.STUDENT_LOCATIONS_TOOL.get('google_map_api_v3_key')
    	course_id = request.POST.get['lis_course_offering_sourcedid']
        enc_user_id = request.POST.get['user_id']

        request.session['lis_course_offering_sourcedid'] = course_id
        request.session['user_id'] = enc_user_id

        return render(request, 'student_locations/map_view.html', {'request': request, 'api_key': key})
    else:
        return render(request, 'student_locations/error.html', {'message': 'Error: user is not authenticated!'})

#@login_required()
#@require_http_methods(['GET'])
#def main(request):
    #key = settings.STUDENT_LOCATIONS_TOOL.get('google_map_api_v3_key')
    #logger.debug('In main')
#    return render(request, 'student_locations/map_view_new.html', {'request': request, 'api_key': key})


@login_required()
@require_http_methods(['GET'])
def user_edit_view(request):
    
    course_id = request.session['LTI_LAUNCH']['lis_course_offering_sourcedid']
    enc_user_id = request.session['LTI_LAUNCH']['user_id']

    logger.debug('In user_edit_view : course_id='+course_id)

    try:
        student = Locations.objects.get(course_id=course_id, user_id=enc_user_id)
    except Locations.DoesNotExist:
        student = None

    if student:
        form = StudentLocationForm(instance=student)
    else:
        logger.debug('student is None')
        form = StudentLocationForm()

    return render(request, 'student_locations/user_edit_view.html', {'request': request, 'form': form})

@login_required()
def addoredituser(request):
    
    course_id = request.session['lis_course_offering_sourcedid']
    enc_user_id = request.session['user_id']

    logger.debug('In addoredituser : course_id='+course_id)

    try:
        student = Locations.objects.get(course_id=course_id, user_id=enc_user_id)
    except Locations.DoesNotExist:
        student = None

    if student:
        form = StudentLocationForm(instance=student, user_id=enc_user_id, course_id=course_id, data=request.POST)
    else:
        logger.debug('student is None')
        form = StudentLocationForm(user_id=enc_user_id, course_id=course_id, data=request.POST)

    logger.debug('form is valid: '+ str(form.is_valid()))

    if form.is_valid():
        theform = form.save(commit=False)
        theform.user_id = enc_user_id
        theform.course_id = course_id
        theform.save()
        key = settings.STUDENT_LOCATIONS_TOOL.get('google_map_api_v3_key')
        return render(request, 'student_locations/map_view.html', {'request': request, 'api_key' : key})
    else:
        return render(request, 'student_locations/user_edit_view.html', {'request': request, 'form': form})

@login_required()
@require_http_methods(['GET'])
def table_view(request):
    
    course_id = request.session['lis_course_offering_sourcedid']
    students = Locations.objects.filter(course_id=course_id)
    logger.debug('course_id: '+course_id)
    return render(request, 'student_locations/table_view.html', {'request': request, 'data' : students})

@login_required()
@require_http_methods(['GET'])
def markers_class_xml(request):
      
    course_id = request.session['lis_course_offering_sourcedid']
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





