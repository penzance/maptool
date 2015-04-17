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
    label="Enter a description for this view.",
    max_length=250,
    required=True,
    )

    def __init__(self, context_id=None, custom_canvas_course_id=None, resource_link_id=None, *args, **kwargs):
        super(ItemGroupForm, self).__init__(*args, **kwargs)
        self._context_id = context_id
        self._custom_canvas_course_id = custom_canvas_course_id
        self._resource_link_id = resource_link_id
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.help_text_inline = True
        self.helper.render_unmentioned_fields = True
        self.helper.form_action = 'toolinstanceconfig'
        self.helper.form_error_title = u"There were problems with the information you submitted."
        self.helper.layout = Layout(
            Div(
            HTML("""
                <h3>Tool Instance Configuration</h3>
                <p class="help-block">Please fill in the following information about the view you would like to create.
                You must give the view a title and short description.</p>
                """)
            , css_class="text-box"),
            Div(
                Fieldset(
                    'Create a new view',
                    'item_name',
                    'item_description'
                ),
                css_class="location-box"),
            Div(
                 FormActions(
                     Submit('saveitemgroup', 'Next page', css_class='btn-primary'),
                     Button('cancel', 'Cancel')

                 )
                 , css_class="text-box")
        )

class UrlForm(forms.ModelForm):
        class Meta:
            model = Urls
            exclude = ['itemgroup', 'generated_longitude_1', 'generated_latitude_1','generated_longitude_2', 'generated_latitude_2', 'generated_longitude_3', 'generated_latitude_3', 'zoom_1', 'zoom_2', 'zoom_3']

        generated_longitude_1 = forms.CharField(required=False, widget=forms.HiddenInput())
        generated_latitude_1 = forms.CharField(required=False, widget=forms.HiddenInput())
        generated_longitude_2 = forms.CharField(required=False, widget=forms.HiddenInput())
        generated_latitude_2 = forms.CharField(required=False, widget=forms.HiddenInput())
        generated_longitude_3 = forms.CharField(required=False, widget=forms.HiddenInput())
        generated_latitude_3 = forms.CharField(required=False, widget=forms.HiddenInput())
        zoom_1 = forms.CharField(required=False, widget=forms.HiddenInput())
        zoom_2 = forms.CharField(required=False, widget=forms.HiddenInput())
        zoom_3 = forms.CharField(required=False, widget=forms.HiddenInput())

        url_1 = forms.CharField(
        label="Add the Google Maps URL of the first display you want. (Leave blank for a world map)",
        max_length=250,
        initial='http://www.maps.google.com',
        required=True,
        )

        description_1 = forms.CharField(
        label="Add a description for your first view",
        max_length=250,
        required=False,
        )

        url_2 = forms.CharField(
        label="OPTIONAL Add the Google Maps URL of the second display you want.",
        max_length=250,
        initial='',
        required=False,
        )

        description_2 = forms.CharField(
        label="Add a description for your second view",
        max_length=250,
        required=False,
        )

        url_3 = forms.CharField(
        label="OPTIONAL Add the Google Maps URL of the third display you want.",
        max_length=250,
        initial='',
        required=False,
        )

        description_3 = forms.CharField(
        label="Add a description for your third view",
        max_length=250,
        required=False,
        )

        def __init__(self, *args, **kwargs):
            super(UrlForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            self.helper.form_class = 'form-horizontal'
            self.helper.label_class = 'col-lg-2'
            self.helper.field_class = 'col-lg-8'
            self.helper.form_method = 'post'
            self.helper.help_text_inline = True
            self.helper.render_unmentioned_fields = True
            self.helper.form_action = 'toolinstanceconfig'
            self.helper.form_error_title = u"There were problems with the information you submitted."
            self.helper.layout = Layout(
                Div(
                HTML("""
                    <h3>Tool Instance Configuration</h3>
                    <p class="help-block">You may provide up to three URLs to Google Maps
                    centered on various regions you would like to display. If you do not choose to enter any URLs, the
                    world map will be selected by default.</p>
                    """)
                , css_class="text-box"),
                Div(
                    Fieldset(
                        'Links to Google Maps URLs',
                        'url_1',
                        'description_1',
                        'url_2',
                        'description_2',
                        'url_3',
                        'description_3'
                    ),
                    css_class="location-box"),
                 Div(
                 FormActions(
                     Submit('saveurl', 'Save new view', css_class='btn-primary'),
                     Button('cancel', 'Cancel')

                 )
                 , css_class="text-box")
            )

class LocationForm(forms.ModelForm):
    class Meta:
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
    user_id = forms.CharField(required=False, widget=forms.HiddenInput())

    title = forms.CharField(
        label="Location Name",
        max_length=60,
        required=True,
    )

    info = forms.CharField(
        label="Location Information",
        max_length=50,
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
        self._first_name = first_name
        self._last_name = last_name
        self._user_id = user_id
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.help_text_inline = True
        self.helper.render_unmentioned_fields = True
        self.helper.form_action = 'addoreditlocation'
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

    def clean(self):

        cleaned_data = super(LocationForm, self).clean()
        address = cleaned_data.get('address')
        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')
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
                    print ('check')
                    data = urllib2.urlopen(url).read()
                    print "%s, %s" % (data, "Hello 123")
                    json_data = json.loads(data)
                    print "%s, test 123" % (json_data)
                else:
                    msg = "We were unable to parse lat/long coordinates from the given map url."
                    self._errors["mapurl"] = self.error_class([msg])
                    raise forms.ValidationError(msg)


            except UnicodeError:
                ms = u"UnicodeError in map url"
                self._errors["mapurl"] = self.error_class([msg])
                print ("check after error 1")
                raise forms.ValidationError(msg)
            except IOError:
                msg = u"IOError in map url"
                self._errors["mapurl"] = self.error_class([msg])
                print ("check after error 2")
                raise forms.ValidationError(msg)
            except Exception as e:
                print('%s' % e)
                msg = u"Exception map url"
                self._errors["mapurl"] = self.error_class([msg])
                print ("check after error 3")
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

        # import pdb; pdb.set_trace()
        result = json_data['results'][0]
        cleaned_data['address'] = result['formatted_address']
        cleaned_data['generated_latitude'] = result['geometry']['location']['lat']
        cleaned_data['generated_longitude'] = result['geometry']['location']['lng']
        cleaned_data['user_id'] = self._user_id
        cleaned_data['fist_name'] = self._first_name
        cleaned_data['last_name'] = self._last_name

        for component in result['address_components']:
            if len(component['types']) > 0:
                if component['types'][0] == 'locality':
                    cleaned_data['locality'] = component.get('long_name')
                if component['types'][0] == 'country':
                    cleaned_data['country'] = component.get('short_name')
                if component['types'][0] == 'administrative_area_level_1':
                    cleaned_data['region'] = component.get('short_name')

        logger.debug("clean complete")

        return cleaned_data


    def save(self, commit=True, *args, **kwargs):
        logger.debug("Location save initiated")
        instance = super(LocationForm, self).save(commit=False, *args, **kwargs)

        cleaned_data = self.cleaned_data
        instance.generated_latitude = cleaned_data['generated_latitude']
        instance.generated_longitude = cleaned_data['generated_longitude']
        instance.locality = cleaned_data['locality']
        instance.country = cleaned_data['country']
        instance.region = cleaned_data['region']
        instance.user_id = cleaned_data['user_id']
        instance.first_name = cleaned_data['fist_name']
        instance.last_name = cleaned_data['last_name']

        if commit:
            instance.save()
        return instance

    # def saveitemgroup(self, commit=True, *args, **kwargs):
    #     logger.debug("Item SAVE INITIATED")
    #     instance = super(ItemGroupForm, self).save(commit=False, *args, **kwargs)
    #     if commit:
    #         instance.save()
    #     return instance

    # def testclean(self):
    #     cleaned_url = super(UrlForm, self).testclean()
    #     url_1 = cleaned_url.get('url_1')
    #     try:
    #         urllib.urlopen(url_1)
    #         latlong = getlatlongfromurl(url_1)
    #         print('We got a')
    #         print latlong
    #         print('!!!')
    #
    #         if latlong:
    #             cleaned_url['url_1'] = url_1
    #             url = 'http://maps.googleapis.com/maps/api/geocode/json?latlng='+latlong+'&sensor=true'
    #             print ('check')
    #             data = urllib2.urlopen(url).read()
    #             print "%s, %s" % (data, "Hello 123")
    #             json_data = json.loads(data)
    #             print "%s, test 123" % (json_data)
    #         else:
    #             msg = "We were unable to parse lat/long coordinates from the given map url."
    #             self._errors["mapurl"] = self.error_class([msg])
    #             raise forms.ValidationError(msg)
    #     except UnicodeError:
    #         msg = u"UnicodeError in map url"
    #         self._errors["mapurl"] = self.error_class([msg])
    #         print ("check after error 1")
    #         raise forms.ValidationError(msg)
    #     except IOError:
    #         msg = u"IOError in map url"
    #         self._errors["mapurl"] = self.error_class([msg])
    #         print ("check after error 2")
    #         raise forms.ValidationError(msg)
    #     except Exception as e:
    #         print('%s' % e)
    #         msg = u"Exception map url"
    #         self._errors["mapurl"] = self.error_class([msg])
    #         print ("check after error 3")
    #         raise forms.ValidationError(msg)
    #     return cleaned_url

    # def saveurl(self, commit=True, *args, **kwargs):
    #     logger.debug("URL SAVE INITIATED")
    #     print('Why wont you save?')
    #     instance = super(UrlForm, self).save(commit=False, *args, **kwargs)
    #     instance.testclean()
    #     cleaned_url = self.cleaned_url
    #     instance.generated_latitude_1 = cleaned_url['generated_latitude_1']
    #     instance.generated_longitude_1 = cleaned_url['generated_longitude_1']
    #     if commit:
    #         instance.save()
    #     return instance