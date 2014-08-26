import urlparse

def getlatlongfromurl(mapurl):
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
    if 'lis_course_offering_sourcedid' in request.POST:
        return True

