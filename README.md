student locations
=================

an LTI tool that allows students to add thier location and contact info to a google map

###How to setup this app###

Create or use and exisitng Django project

Clone the git repository to the project

```
git clone https://github.com/penzance/student-locations.git
```

Change into the student_locations directory and run a pip install on the
requirements file.
```
pip install -r requirements.txt
```

Add the app url to the project urls.py file
```
urlpatterns = patterns('',
    ...
    url(r'^student_locations/', include('student_locations.urls', namespace="sl")),

)
```

Add 'student_locations' to the installed apps block in the project settings.py file. You also installed crispy forms as part of the pip install so go ahead and add that as well.
```
INSTALLED_APPS = (
    ...
    'student_locations',
    'crispy_forms',
)
```

Add the following to your project settings.py file
```
STUDENT_LOCATIONS_TOOL = {
    'google_map_api_v3_key': '... your google map key ...',
}

CRISPY_TEMPLATE_PACK = 'bootstrap3'

```

The app uses the Django default sqlite database out of the box, if you want to change this update the database block in your settings.py file. Prepare the app schema by running syncdb, make sure you are in the root of your project where the manage.py 
file is located.
```
python manage.py syncdb
```

Now you should be able to run the app liek this

```
python manage.py runserver 0.0.0.0:8000
```

As long as you don't see any errors you should be able to naviage to the index page. If I am running this on my local machine the using the runserver command above the url would be:
```
http://localhost:8000/student_locations/
```
copy the student_location.js file to your projects static files directory.
