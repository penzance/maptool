from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.http import require_http_methods
from ims_lti_py.tool_config import ToolConfig
from django.conf import settings
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from maptoolapp.forms import LocationForm, ItemGroupForm, UrlForm
from maptoolapp.models import Locations, ItemGroup, Urls
from maptoolapp.utils import (validaterequiredltiparams)
import urllib2
import datetime
from django import forms
from maptoolapp.utils import getlatlongandzoom
from maptoolapp.utils import getparamfromsession
import urllib
import urllib2
import json
from models import Locations, Urls, ItemGroup

import logging


logger = logging.getLogger(__name__)

@require_http_methods(['GET'])
def index(request):
    """
    Show the index file
    """
    return render(request, 'maptoolapp/index.html')

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
            return redirect('maptoolapp:main')
        else:
            return render(request, 'maptoolapp/error.html', {'message': 'Error: The LTI parameter lis_course_offering_sourcedid is required by this LTI tool.'})
    else:
        return render(request, 'maptoolapp/error.html', {'message': 'Error: user is not authenticated!'})

@login_required()
@require_http_methods(['GET'])
def main(request):
    """
    The main method display the default view which is the instance_selection view.
    """
    user_type = getparamfromsession(request, 'roles')
    custom_canvas_course_id = getparamfromsession(request, 'custom_canvas_course_id')

    # Check to make sure that both all itemgroups have a corresponding url  have been submitted
    itemgroup_ids = ItemGroup.objects.all().values('id')
    for itemgroup in itemgroup_ids:
        check_itemgroup = itemgroup.get('id')
        check_url = Urls.objects.filter(itemgroup=check_itemgroup)
        if not check_url.exists():
            ItemGroup.objects.get(id=check_itemgroup).delete()

    data = ItemGroup.objects.filter(custom_canvas_course_id=custom_canvas_course_id)

    if ("Instructor" in user_type) and (data.count() == 0):
        itemgroupform = ItemGroupForm
        return render(request, 'maptoolapp/tool_instance_config.html', {'request':request, 'itemgroupform':itemgroupform})
    elif ("Instructor" not in user_type) and (data.count() == 0):
        return render(request, 'maptoolapp/error.html', {'message': 'Error: The course instructor must configure this tool before it can be accessed.'})
    else:
        return render(request, 'maptoolapp/itemgroup_instance_selection.html', {'request': request, 'data': data})

@login_required()
@require_http_methods(['GET'])
def displaymaps(request, data):
    """
    The main method display the default view which is the map_view.
    """
    request.session['itemgroup_session'] = data
    urls = Urls.objects.get(itemgroup=data)
    itemgroup = ItemGroup.objects.filter(id = data)
    key = settings.MAP_TOOL_APP.get('google_map_api_v3_key')
    user_id = getparamfromsession(request, 'user_id')
    mypoints = Locations.objects.filter(user_id=user_id, itemgroup=data)
    return render(request, 'maptoolapp/map_view_2.html', {'request': request, 'api_key': key, 'urls':urls, 'itemgroup':itemgroup, 'mypoints':mypoints})

@login_required()
@require_http_methods(['GET'])
def mapsview(request):
    """
    Method to display map view if the itemgroup_session has already been set.
    """
    user_id = getparamfromsession(request, 'user_id')
    itemgroup_session = request.session.get('itemgroup_session')
    urls = Urls.objects.get(itemgroup=itemgroup_session)
    itemgroup = ItemGroup.objects.filter(id = itemgroup_session)
    key = settings.MAP_TOOL_APP.get('google_map_api_v3_key')
    mypoints = Locations.objects.filter(user_id=user_id, itemgroup=itemgroup_session)
    return render(request, 'maptoolapp/map_view_2.html', {'request': request, 'api_key': key, 'urls':urls, 'itemgroup':itemgroup, 'mypoints':mypoints})

@login_required()
@require_http_methods(['GET'])
def add_location(request):
    """
    Displays the add location view which allows users to enter locations
    and descriptions for display on the Google map.
    """
    resource_link_id = getparamfromsession(request, 'resource_link_id')
    user_id = getparamfromsession(request, 'user_id')
    if not resource_link_id or not user_id:
        return render(request, 'maptoolapp/error.html', {'message': 'Unable to retrieve params from session. You might want to try reloading the tool.'})

    locationform = LocationForm

    return render(request, 'maptoolapp/add_location.html', {'request': request, 'locationform': locationform})

@login_required()
@require_http_methods(['POST'])
def deleteview(request):
    """
    Allows an instructor to delete a view from the tool.
    """
    theclass = request.POST.get('class')
    data = request.POST.get('id')
    if theclass == 'deleteRow':
        ItemGroup.objects.filter(id=data).delete()
        return HttpResponse('')
    else:
        Locations.objects.filter(id=data).delete()
        itemgroup_session = request.session.get('itemgroup_session')
        urls = Urls.objects.get(itemgroup=itemgroup_session)
        itemgroup = ItemGroup.objects.filter(id = itemgroup_session)
        key = settings.MAP_TOOL_APP.get('google_map_api_v3_key')
        user_id = getparamfromsession(request, 'user_id')
        mypoints = Locations.objects.filter(user_id=user_id, itemgroup=itemgroup_session)
        return render(request, 'maptoolapp/map_view_2.html', {'request': request, 'api_key': key, 'urls':urls, 'itemgroup':itemgroup, 'mypoints':mypoints})

@login_required()
def addoreditlocation(request):
    """
    The action method for the user_edit_view form.
    """
    enter_user_id = getparamfromsession(request, 'user_id')
    lis_person_name_family = getparamfromsession(request, 'lis_person_name_family')
    lis_person_name_given = getparamfromsession(request, 'lis_person_name_given')

    locationform = LocationForm(first_name=lis_person_name_given, last_name=lis_person_name_family, user_id=enter_user_id, data=request.POST)
    itemgroup_session = request.session.get('itemgroup_session')

    if locationform.is_valid():
        user_id = getparamfromsession(request, 'user_id')
        itemgroup_session = request.session.get('itemgroup_session')
        mypoints = Locations.objects.filter(user_id=user_id, itemgroup=itemgroup_session)
        urls = Urls.objects.get(itemgroup=itemgroup_session)
        itemgroup = ItemGroup.objects.filter(id = itemgroup_session)
        theform = locationform.save(commit=False)
        theform.itemgroup = ItemGroup.objects.get(id=itemgroup_session)
        theform.first_name = lis_person_name_given
        theform.last_name = lis_person_name_family
        theform.user_id = enter_user_id
        theform.datetime = datetime.datetime.now()
        theform.save()
        key = settings.MAP_TOOL_APP.get('google_map_api_v3_key')
        return render(request, 'maptoolapp/map_view_2.html', {'request': request, 'api_key': key, 'urls':urls, 'itemgroup':itemgroup, 'mypoints':mypoints})
    else:
        return render(request, 'maptoolapp/add_location.html', {'request': request, 'locationform': locationform})

@login_required()
def toolinstanceconfig(request):
    """
    The action method for the configuring a new instance of the tool.
    """
    context_id = getparamfromsession(request, 'context_id')
    custom_canvas_course_id = getparamfromsession(request, 'custom_canvas_course_id')
    resource_link_id = getparamfromsession(request, 'resource_link_id')

    itemgroupform = ItemGroupForm(context_id=context_id, custom_canvas_course_id=custom_canvas_course_id, resource_link_id=resource_link_id, data=request.POST)
    urlform = UrlForm(data=request.POST)
    if request.POST:
        if itemgroupform.is_valid():
            theitemform = itemgroupform.save(commit=False)
            theitemform.context_id = context_id
            theitemform.custom_canvas_course_id = custom_canvas_course_id
            theitemform.resource_link_id = resource_link_id
            theitemform.save()
            request.session['itemgroup_session'] = theitemform.id
            render_url_form = UrlForm
            return render(request, 'maptoolapp/tool_instance_config_2.html', {'request': request, 'urlform': render_url_form})
        elif urlform.is_valid():
            itemgroupform = ItemGroup.objects.get(id=request.session.get('itemgroup_session'))
            theurlform = urlform.save(commit=False)
            url_1 = theurlform.url_1
            url_2 = theurlform.url_2
            url_3 = theurlform.url_3

            if url_1:
                try:
                    urllib.urlopen(url_1)
                    latlong_1, zoom_1 = getlatlongandzoom(url_1)
                    print latlong_1
                    print('2') * 60

                    if latlong_1:
                        test_url_1 = 'http://maps.googleapis.com/maps/api/geocode/json?latlng='+latlong_1+'&sensor=true'
                        data_1 = urllib2.urlopen(test_url_1).read()
                        json_data_1 = json.loads(data_1)
                        print json_data_1
                        print('1') * 60
                    # else:
                        # breakbreak
                        # msg = "1 We were unable to parse lat/long coordinates from the given map urls. Try again"
                        # raise forms.ValidationError(msg)
                except UnicodeError:
                    msg = u"UnicodeError in map url"
                    self._errors["mapurl"] = self.error_class([msg])
                    raise forms.ValidationError(msg)
                except IOError:
                    msg = u"1IOError in map url"
                    raise forms.ValidationError(msg)

                result_1 = json_data_1['results'][0]
                theurlform.generated_longitude_1 = result_1['geometry']['location']['lng']
                theurlform.generated_latitude_1 = result_1['geometry']['location']['lat']
                theurlform.zoom_1 = zoom_1

            if url_2:
                length = len(url_2)
                print('@') * 100
                print length
                print('$') * 100
                try:
                    urllib.urlopen(url_2)
                    latlong_2, zoom_2 = getlatlongandzoom(url_2)

                    if latlong_2:
                        test_url_2 = 'http://maps.googleapis.com/maps/api/geocode/json?latlng='+latlong_2+'&sensor=true'
                        data_2 = urllib2.urlopen(test_url_2).read()
                        json_data_2 = json.loads(data_2)
                    # else:
                    #     break
                        # msg = "2 We were unable to parse lat/long coordinates from the given map urls. Try again"
                        # raise forms.ValidationError(msg)
                except UnicodeError:
                    msg = u"UnicodeError in map url"
                    self._errors["mapurl"] = self.error_class([msg])
                    raise forms.ValidationError(msg)
                except IOError:
                    msg = u"2IOError in map url"
                    raise forms.ValidationError(msg)

                result_2 = json_data_2['results'][0]
                theurlform.generated_longitude_2 = result_2['geometry']['location']['lng']
                theurlform.generated_latitude_2 = result_2['geometry']['location']['lat']
                theurlform.zoom_2 = zoom_2

            if url_3:
                try:
                    urllib.urlopen(url_3)
                    latlong_3, zoom_3 = getlatlongandzoom(url_3)

                    if latlong_3:
                        test_url_3 = 'http://maps.googleapis.com/maps/api/geocode/json?latlng='+latlong_3+'&sensor=true'
                        data_3 = urllib2.urlopen(test_url_3).read()
                        json_data_3 = json.loads(data_3)
                    # else:
                    #     break
                        # msg = "We were unable to parse lat/long coordinates from the given map urls. Try again"
                        # raise forms.ValidationError(msg)

                except UnicodeError:
                    msg = u"UnicodeError in map url"
                    self._errors["mapurl"] = self.error_class([msg])
                    raise forms.ValidationError(msg)
                except IOError:
                    msg = u"3IOError in map url"
                    raise forms.ValidationError(msg)

                result_3 = json_data_3['results'][0]
                theurlform.generated_longitude_3 = result_3['geometry']['location']['lng']
                theurlform.generated_latitude_3 = result_3['geometry']['location']['lat']
                theurlform.zoom_3 = zoom_3

            theurlform.itemgroup = itemgroupform
            theurlform.save()

            # Check to make sure that both the itemgroup and url forms have been submitted
            itemgroup_session = request.session.get('itemgroup_session')
            check_url = Urls.objects.filter(itemgroup=itemgroup_session)
            if not check_url.exists():
                ItemGroup.objects.get(id=itemgroup_session).delete()

            data = ItemGroup.objects.all()
            return render(request, 'maptoolapp/itemgroup_instance_selection.html', {'request': request, 'data': data})
        else:
            return render(request, 'maptoolapp/error.html', {'message': 'Error: please refresh and try configuring the tool again'})
    else:
        itemgroupform = ItemGroupForm
        data = ItemGroup.objects.filter(custom_canvas_course_id = custom_canvas_course_id)
        count = data.count()
        return render(request, 'maptoolapp/tool_instance_config.html', {'request':request, 'itemgroupform':itemgroupform, 'data':data, 'count':count})
@login_required()
@require_http_methods(['GET'])
def table_view(request):
    """
    renders the data and display of the table view of students
    """
    itemgroup_session = request.session.get('itemgroup_session')
    locationlist = Locations.objects.filter(itemgroup = itemgroup_session)
    return render(request, 'maptoolapp/table_view.html', {'request': request, 'data': locationlist})

@login_required()
@require_http_methods(['GET'])
def markers_class_xml(request):
    """
    renders the XML containing the location data for the google map
    """
    itemgroup_session = request.session.get('itemgroup_session')
    locationlist = Locations.objects.filter(itemgroup = itemgroup_session)
    return render_to_response('maptoolapp/markers.xml', {'data': locationlist}, context_instance=RequestContext(request))

@login_required()
@require_http_methods(['GET'])
def header(request):
    """
    renders a header
    """
    user_type = getparamfromsession(request, 'roles')
    if ("Instructor" in user_type):
        role = 'instructor'
    else:
        role = 'student'
    return render('maptoolapp/header.html', {'role': role})

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

    url = host + reverse('maptoolapp:lti_launch')

    lti_tool_config = ToolConfig(
        title='Map Tool',
        launch_url=url,
        secure_launch_url=url,
    )
    account_nav_params = {
        'enabled': 'true',
        # optionally, supply a different URL for the link:
        # 'url': 'http://library.harvard.edu',
        'text': 'Map Tool',
    }
    lti_tool_config.set_ext_param('canvas.instructure.com', 'privacy_level', 'public')
    lti_tool_config.set_ext_param('canvas.instructure.com', 'course_navigation', account_nav_params)
    lti_tool_config.description = 'This LTI tool facilitates the gathering pins for many similar locations on a map.'

    resp = HttpResponse(lti_tool_config.to_xml(), content_type='text/xml', status=200)
    return resp