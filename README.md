student-locations
=================

an LTI tool that allows students to add thier location and contact info to a google map

Add 'student_locations' to the installed apps block in the project settings.py file
```
INSTALLED_APPS = (
    ...
    'student_locations',
)
```
Add the following to your project settings.py file
```
STUDENT_LOCATIONS_TOOL = {
    'google_map_api_v3_key': '... your google map key ...',
}

CRISPY_TEMPLATE_PACK = 'bootstrap3'

LTI_OAUTH_CREDENTIALS = { 'changeme' : 'changeme', }
```

The app uses the Django default sqlite database out of the box, if you want to change this update the database block in your settings.py file.

