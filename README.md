student locations
=================

an LTI tool that allows students to add thier location and contact info to a google map

###How to setup this app###

Create or use and exisitng Django project


To make it as easy as possible to get up and running, I've included a sample settings.py file called settings.py.sample
and a sample secure.py file called secure.py.sample. Secure.py will contain your secure settings that should be not checked into
git (there is a line in the .gitignore to ignore this file). 

To get started, create a new django project

```
django-admin.py startproject myproject
```

Clone the git repository to the project

```
cd myproject
git clone https://github.com/penzance/student-locations.git
```

Now run a pip install on the
requirements file.
```
pip install -r student_locations/requirements.txt
```

Move the folder called static to the root of the project.
You should still be in the myproject folder. Then run the collectstatic process.
```
mv student_locations/static .
python manage.py collectstatic
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

