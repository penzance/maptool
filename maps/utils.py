
from django.conf import settings

def validaterequiredltiparams(request):
    """
    verify that the required LTI parameters are present in the request object.
    """
    lti_launch = set(request.session.get('LTI_LAUNCH'))
    required_params = set(settings.MAPS.get('required_lti_params'))
    return required_params.issubset(lti_launch)

def getparamfromsession(request, param):
    lti_launch = request.session.get('LTI_LAUNCH')
    return lti_launch.get(param)

