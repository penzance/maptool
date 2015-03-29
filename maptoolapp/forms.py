from datetime import datetime, time, date
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit, ButtonHolder, Button, HTML, Div
from crispy_forms.bootstrap import FormActions
from django.core.validators import validate_email, MaxValueValidator, MinValueValidator, RegexValidator
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from maptoolapp.utils import getlatlongfromurl
from maptoolapp.utils import getparamfromsession
from django.contrib.admin import widgets 
import urllib
import urllib2
import urlparse
import json
from django.forms import ModelForm
from models import Locations, Urls, ItemGroup

import logging
logger = logging.getLogger(__name__)

class ItemGroupForm(forms.ModelForm):

    class Meta:
        model = ItemGroup
        exclude = ['resource_link_id', 'context_id', 'custom_canvas_course_id']


    resource_link_id = forms.CharField(required=False, widget=forms.HiddenInput())
    context_id = forms.CharField(required=False, widget=forms.HiddenInput())
    custom_canvas_course_id = forms.CharField(required=False, widget=forms.HiddenInput())

    item_name = forms.CharField(
    label="Enter the title of this view.",
    max_length=50,
    required=True,
    )

    item_description = forms.CharField(
    widget = forms.Textarea,
    label="Enter a description for this view.",
    required=True,
    )

    def __init__(self, user_id=None, resource_link_id=None, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self._resource_link_id = resource_link_id

class UrlForm(forms.ModelForm):

        class Meta:
            model = Urls
            exclude = ['itemgroup']

        itemgroup = forms.CharField(required=False, widget=forms.HiddenInput())

        url_1 = forms.CharField(
        label="Add the Google Maps URL of the first display you want. (Leave blank for a world map)",
        max_length=50,
        initial='http://www.maps.google.com',
        required=False,
        )

        url_2 = forms.CharField(
        label="OPTIONAL Add the Google Maps URL of the second display you want.",
        max_length=50,
        required=False,
        )

        url_3 = forms.CharField(
        label="OPTIONAL Add the Google Maps URL of the third display you want.",
        max_length=50,
        required=False,
        )

class LocationForm(forms.ModelForm):

    class Meta:
        model = Locations

        model = Locations
        exclude = ['method', 'generated_latitude', 'generated_longitude', 'locality', 'region', 'country', 'datetime', 'itemgroup', 'user_id', 'first_name', 'last_name']

    locality = forms.CharField(required=False, widget=forms.HiddenInput())
    region = forms.CharField(required=False, widget=forms.HiddenInput())
    country = forms.CharField(required=False, widget=forms.HiddenInput())
    generated_longitude = forms.CharField(required=False, widget=forms.HiddenInput())
    generated_latitude = forms.CharField(required=False, widget=forms.HiddenInput())
    method = forms.CharField(required=False, widget=forms.HiddenInput())
    datetime = forms.CharField(required=False, widget=forms.HiddenInput())
    first_name = forms.CharField(required=False, widget=forms.HiddenInput())
    last_name = forms.CharField(required=False, widget=forms.HiddenInput())
    #TODO
    # itemgroup = forms.CharField(required=False, widget=forms.HiddenInput())
    user_id = forms.CharField(required=False, widget=forms.HiddenInput())

    title = forms.CharField(
    label="Location Name",
    max_length=60,
    required=True,
    )

    info = forms.CharField(
    label="Location Information",
    max_length=250,
    required=True,
    )

    address = forms.CharField(
        label="Address",
        max_length=60,
        required=False,
    )
  
    latitude = forms.CharField(label="Latitude", required=False)
    longitude = forms.CharField(label="Longitude", required=False)

    mapurl = forms.CharField(
        label="Google Map URL",
        max_length=200,
        required=False,
    )

    def __init__(self, first_name=None, last_name=None, user_id=None, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.help_text_inline = True
        self.helper.render_unmentioned_fields = True
        self.helper.form_action = 'addoredituser'
        self.helper.form_error_title = u"There were problems with the information you submitted."
        
        self.helper.layout = Layout(
            Div(
            HTML("""
                <h3>Location</h3>
                <p class="help-block">Please fill in <strong>one</strong> of the following:</p>
                <ul class="help-block">
                    <li>Address</li>
                    <li>Latitude and Longitude</li>
                    <li>Google Map URL that is centered on your location</li>
                </ul>
                <p class="help-block">If you don't wish to provide your work or home location,
                you can give a more general location such as your favorite
                lunch spot, park, or just the center of your city or
                town.</p>
                """)
            , css_class="text-box"),
            Div(
                Fieldset(
                    'Title',
                    'title',
                    'Location Information',
                    'info'
                ),
                HTML("""
                    <p class="help-block">
                        Provide a clear title for the landmark and a brief description of the location.
                    """)
                , css_class="location-box"),
            Div(
                Fieldset(
                    'Address',
                    'address'
                ),
                HTML("""
                    <p class="help-block">
                        Street (optional), City, State, Country 
                        e.g. "1 Oxford St, Cambridge, MA", "Lawrence, KS" or
                        "Paris, France"</p>
                    """)
            , css_class="location-box"),
            Div(
                Fieldset(
                    'Latitude and Longitude',
                    'latitude',
                    'longitude'
                ),
                HTML("""
                    <p class="help-block">Use decimal degrees only and negative numbers for
                    "South" (e.g. 42.3762 and not 42&deg; 22' 34" N ).</p>
                    """)
            , css_class="location-box"),
            Div(
                Fieldset(
                    'Google Map URL',
                    'mapurl'
                ),
                HTML("""
                    <p class="help-block">Cut and paste the Google Map URL that is centered on
                    your location.<br />

                        <ul class="help-block">
                            <li>Click on the map to center it</li>
                            <li>Click on "Link to this page"</li>
                            <li>Cut-and-paste the resulting URL</li>
                        </ul>
                    </p>
                    """)
            , css_class="location-box"),
            Div(
            FormActions(
                Submit('save', 'Save new location', css_class='btn-primary'),
                Button('cancel', 'Cancel')
                
            )
            , css_class="text-box")
        )
        

    @property
    def clean(self):

        cleaned_data = super(LocationForm, self).clean()
        address = cleaned_data.get('address') 
        latitude = cleaned_data.get('latitude') 
        longitude = cleaned_data.get('longitude')
        info = cleaned_data.get('info')
        title = cleaned_data.get('title')
        mapurl = cleaned_data.get('mapurl')

        if len(address) > 0 and address != 'None':
            cleaned_data['method'] = 'address'
            address = urllib.quote_plus(cleaned_data.get('address'))
            url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+address+'&sensor=true'

            data = urllib2.urlopen(url).read()
            json_data = json.loads(data)
            status = json_data.get('status')
            logging.debug(status)
            if status != 'OK':
                msg = "No results were found for the given address"
                self._errors["address"] = self.error_class([msg])
                raise forms.ValidationError(msg)

        elif len(mapurl) > 0 and mapurl != 'None':
            cleaned_data['method'] = 'mapurl'
            
            # We validate that we got a real url and not just a string of data
            try:
                urllib.urlopen(mapurl)
                #query = urlparse.urlparse(mapurl).query
                #query_dict = urlparse.parse_qs(query)
                #https://www.google.com/maps/@42.2733204,-83.7376894,12z
                # https://www.google.com/maps/place/Antarctica/@-75,0,2z/data=!3m1!4b1!4m2!3m1!1s0xb09dff882a7809e1:0xb08d0a385dc8c7c7

                latlong = getlatlongfromurl(mapurl)
                print latlong
                            
                if latlong:
                    cleaned_data['mapurl'] = mapurl
                    url = 'http://maps.googleapis.com/maps/api/geocode/json?latlng='+latlong+'&sensor=true'
                    data = urllib2.urlopen(url).read()
                    json_data = json.loads(data)
                else:
                    msg = "We were unable to parse lat/long coordinates from the given map url."
                    self._errors["mapurl"] = self.error_class([msg])
                    raise forms.ValidationError(msg)
                    

            except UnicodeError:
                ms = u"UnicodeError in map url"
                self._errors["mapurl"] = self.error_class([msg])
                raise forms.ValidationError(msg)
            except IOError:
                msg = u"IOError in map url"
                self._errors["mapurl"] = self.error_class([msg])
                raise forms.ValidationError(msg)
            except Exception as e:
                print('%s' % e)
                msg = u"Exception map url"
                self._errors["mapurl"] = self.error_class([msg])
                raise forms.ValidationError(msg)
                
        elif len(latitude) > 0  and len(longitude) > 0 and latitude != 'None' and longitude != 'None':
            cleaned_data['method'] = 'latlong'
            
            # Below we check to see if we got valid floating point numbers for the lat long coords.
            # If not we throw and exception.
            
            try:
                latitude_float_test = float(latitude)
            except ValueError:
                msg = u"Invalid latitude value. Latitude must be in decimal degrees  (e.g. 42.3762)"
                self._errors["latitude"] = self.error_class([msg])
                raise forms.ValidationError(msg)

            try:
                longitude_float_test = float(longitude)
            except ValueError:
                msg = u"Invalid longitude value. Longitude must be in decimal degrees  (e.g. 42.3762)"
                self._errors["longitude"] = self.error_class([msg])
                raise forms.ValidationError(msg)

            
            # We need to build the google geocode query string and see if we get good data.
            # If not we throw and exception.
            
            latlong = latitude + ',' + longitude 
            # http://maps.googleapis.com/maps/api/geocode/json?latlng=32.381499,-62.319492&sensor=true
            url = 'http://maps.googleapis.com/maps/api/geocode/json?latlng='+latlong+'&sensor=true'
            data = urllib2.urlopen(url).read()
            json_data = json.loads(data)

            status = json_data['status']
            if status != 'OK':
                msg = u"No results were found for the given coordinates"
                self._errors["longitude"] = self.error_class([msg])
                self._errors["latitude"] = self.error_class([msg])
                raise forms.ValidationError(msg)

        else:
            
            # The user did not enter any values for any of the geocoding fields (i.e address, lat/long. mapurl)
            # so we throw and exception.
            
            cleaned_data['method'] = 'None'
            msg = u"You must enter one of the following"
            self._errors["address"] = self.error_class([msg])
            self._errors["latitude"] = self.error_class([msg])
            self._errors["longitude"] = self.error_class([msg])
            self._errors["mapurl"] = self.error_class([msg])
            raise forms.ValidationError(msg)
        
        result = json_data['results'][0]   
        cleaned_data['address'] = result['formatted_address']       
        cleaned_data['generated_latitude'] = result['geometry']['location']['lat']
        cleaned_data['generated_longitude'] = result['geometry']['location']['lng']

        for component in result['address_components']:
            if len(component['types']) > 0:
                if component['types'][0] == 'locality':
                    cleaned_data['locality'] = component.get('long_name')
                if component['types'][0] == 'country':
                    cleaned_data['country'] = component.get('short_name')
                if component['types'][0] == 'administrative_area_level_1':
                    cleaned_data['region'] = component.get('short_name')

        #cleaned_data['user_id'] = self._user_id
        #cleaned_data['itemgroup_id'] = self._itemgroup_id
        #cleaned_data['title'] = self._title
        #cleaned_data['info'] = self._info
        #for key,value in cleaned_data.items():
        #    logger.debug('Key: '+key+', Value='+str(value))

        logger.debug("clean complete")

        return cleaned_data

    def save(self, commit=True, *args, **kwargs):
        logger.debug("save initiated")
        instance = super(LocationForm, self).save(commit=False, *args, **kwargs)

        cleaned_data = self.cleaned_data
        instance.generated_latitude = cleaned_data['generated_latitude']
        instance.generated_longitude = cleaned_data['generated_longitude']
        instance.locality = cleaned_data['locality']
        instance.country = cleaned_data['country']
        instance.region = cleaned_data['region']

        if commit:
            instance.save()
        return instance