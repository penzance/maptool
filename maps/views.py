from django.shortcuts import render, redirect
from maps.utils import (validaterequiredltiparams,
                        getparamfromsession)
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from ims_lti_py.tool_config import ToolConfig

# Create your views here.

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

    url = host + reverse('maps:lti_launch')

    lti_tool_config = ToolConfig(
        title='Maps',
        launch_url=url,
        secure_launch_url=url,
    )
    account_nav_params = {
        'enabled': 'true',
        # optionally, supply a different URL for the link:
        # 'url': 'http://library.harvard.edu',
        'text': 'Maps',
    }
    lti_tool_config.set_ext_param('canvas.instructure.com', 'privacy_level', 'public')
    lti_tool_config.set_ext_param('canvas.instructure.com', 'course_navigation', account_nav_params)
    lti_tool_config.description = 'This LTI tool facilitates the gathering pins for many similar locations on a map.'

    resp = HttpResponse(lti_tool_config.to_xml(), content_type='text/xml', status=200)
    return resp


@require_http_methods(['GET'])
def index(request):
    """
    Show the index file
    """
    return render(request, 'maps/main.html')

@login_required()
@require_http_methods(['POST'])
def lti_launch(request):
    """
    This method is here to build the LTI_LAUNCH dictionary containing all
    the LTI parameters and place it into the session. This is necessary as we
    need to access these parameters throughout the application and they are only
    available the first time the application loads.
    """
    if request.user.is_authenticated():
        if validaterequiredltiparams(request):
            return redirect('maps:main')
        else:
            return render(request, 'maps/error.html', {'message': 'Error: The LTI parameter '
                                                                  'lis_course_offering_sourcedid is '
                                                                  'required by this LTI tool.'})
    else:
        return render(request, 'maps/error.html', {'message': 'Error: user is not authenticated!'})


@login_required()
@require_http_methods(['GET'])
def main(request):

    admin = False
    user_type = getparamfromsession(request, 'roles')
    custom_canvas_course_id = getparamfromsession(request, 'custom_canvas_course_id')

    if "Instructor" in user_type:
        admin = True

    return render(request, 'maps/main.html', {'request': request,
                                              'user_is_admin' : admin,
                                              'course_id': custom_canvas_course_id,})
