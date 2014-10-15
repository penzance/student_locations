import urlparse
from django.conf import settings

def getlatlongfromurl(mapurl):
    """
    try to parse the lat/long data from the mapurl
    """
    query = urlparse.urlparse(mapurl).query
    query_dict = urlparse.parse_qs(query)
    if 'll' in query_dict:
        return query_dict['ll'][0]
    elif '@' in mapurl:
        path = urlparse.urlparse(mapurl).path
        for part in path.split('/'):
            if '@' in part:
                latlonglist = part.split(',')
                if len(latlonglist) == 3:
                    latlonglist.pop()
                    return ','.join(latlonglist)[1:]
    
def validaterequiredltiparams(request):
    """
    verify that the required LTI parameters are present in the request object.
    """
    lti_launch = set(request.session.get('LTI_LAUNCH'))
    required_params = set(settings.STUDENT_LOCATIONS_TOOL.get('required_lti_params'))
    return required_params.issubset(lti_launch)
    

def getparamfromsession(request, param):
    lti_launch = request.session.get('LTI_LAUNCH')
    return lti_launch.get(param)


def check_resource_link_id(resource_link_id, request_resource_link_id):
    """
    This helper method is to check that resource_link_id from most recent 
    lti launch matches the one from  the request. 
    """
    if resource_link_id == request_resource_link_id:
        return True
    return False    

