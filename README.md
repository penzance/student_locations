student locations
=================

an LTI tool that allows students to add thier location and contact info to a google map

###How to setup this app###

Create or use and exisitng Django project


To make it as easy as possible to get up and running, I've included a sample settings.py file called settings.py.sample
and a sample secure.py file called secure.py.sample. Secure.py will contain your secure settings that should be not checked into
git (there is a line in the .gitignore file to ignore the secure.py file). 

To get started, create a new django project.

```
django-admin.py startproject myproject
```

Clone the git repository to the project

```
cd myproject
git clone https://github.com/penzance/student-locations.git
```

Copy the settings.py.sample and secure.py.sample to the project folder. If you are in the new project folder called myproject, there should be a folder there also called myproject. This is where you want to copy the files.

```
cd myproject
You should now be under two levels of myproject (myproject/myproject)
cp ../student_locations/settings.py.sample .
cp ../student_locations/secure.py.sample .
```

Now make a backup of the original settings.py file

```
cp settings.py settings.py.backup
```

Now renames the files

```
mv settings.py.sample settings.py
mv secure.py.sample secure.py
now cd back up to the root project folder
cd ..
```
(You will need to fill in the secure values in the secure.py file)

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
To add the tool to your LMS user the lti_launch url
```
http://localhost:8000/student_locations/lti_launch
```

If you are using Canvas you can also use the tool_config url an choose paste XML to add the tool.
```
http://localhost:8000/student_locations/tool_config
```
