from datetime import datetime, time, date
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit, ButtonHolder, Button, HTML, Div
from crispy_forms.bootstrap import FormActions
from django.core.validators import validate_email, MaxValueValidator, MinValueValidator, RegexValidator
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from student_locations.utils import getlatlongfromurl
import urllib
import urllib2
import urlparse
import json
from django.forms import ModelForm
from models import Locations

import logging
logger = logging.getLogger(__name__)


class StudentLocationForm(forms.ModelForm):

    class Meta:
        model = Locations
        exclude = ['user_id', 'method', 'generated_latitude', 'generated_longitude', 'locality', 'region', 'resource_link_id', 'country']


    user_id = forms.CharField(required=False, widget=forms.HiddenInput())
    resource_link_id = forms.CharField(required=False, widget=forms.HiddenInput())
    locality = forms.CharField(required=False, widget=forms.HiddenInput())
    region = forms.CharField(required=False, widget=forms.HiddenInput())
    country = forms.CharField(required=False, widget=forms.HiddenInput())
    generated_longitude = forms.CharField(required=False, widget=forms.HiddenInput())
    generated_latitude = forms.CharField(required=False, widget=forms.HiddenInput())

    first_name = forms.CharField(
        label="First Name",
        max_length=60,
        required=True,
    )

    first_name_permission = forms.BooleanField(
        label="Display to class members",
        initial=True,
        required=False,
    )

    last_name = forms.CharField(
        label="Last Name",
        max_length=60,
        required=True,
    )

    last_name_permission = forms.BooleanField(
        label="Display to class members",
        initial=True,
        required=False,
    )

    email = forms.EmailField()

    email_permission = forms.BooleanField(
        label="Display to class members",
        initial=True,
        required=False,
    )

    organization = forms.CharField(
        label="Company or Organization",
        max_length=60,
        required=False,
    )

    organization_permission = forms.BooleanField(
        label="Display to class members",
        initial=True,
        required=False,
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

    def __init__(self, user_id=None, resource_link_id=None, *args, **kwargs):
        super(StudentLocationForm, self).__init__(*args, **kwargs)
        self._user_id = user_id
        self._resource_link_id = resource_link_id
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
                <p class="help-block">
            Your location may, but need not pin-point your home or work --
            pick something in the general area of where you are; perhaps a
            favorite park, recreation spot, or restaurant, or the
           'geographic' center of the town in which you live or work.
          </p>
          """)
            , css_class="text-box"),
            Div(
            Fieldset(
                'Information about You',
                'first_name', 'first_name_permission',
                'last_name', 'last_name_permission',
                'email', 'email_permission',
                'organization', 'organization_permission',
            )
            , css_class="location-box"),
            
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
                Submit('save', 'Save changes', css_class='btn-primary'),
                Button('cancel', 'Cancel')
                
            )
            , css_class="text-box")
        )
        

    def clean(self):

        cleaned_data = super(StudentLocationForm, self).clean()
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
                print '%s' % e
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

        cleaned_data['user_id'] = self._user_id
        cleaned_data['resource_link_id'] = self._resource_link_id

        #for key,value in cleaned_data.items():
        #    logger.debug('Key: '+key+', Value='+str(value))

        logger.debug("clean complete")

        return cleaned_data

    def save(self, commit=True, *args, **kwargs):
        instance = super(StudentLocationForm, self).save(commit=False, *args, **kwargs)

        cleaned_data = self.cleaned_data
        instance.generated_latitude = cleaned_data['generated_latitude']
        instance.generated_longitude = cleaned_data['generated_longitude']
        instance.locality = cleaned_data['locality']
        instance.country = cleaned_data['country']
        instance.region = cleaned_data['region']

        if commit:
            instance.save()
        return instance


                    

