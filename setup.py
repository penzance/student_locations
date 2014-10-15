import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
LICENSE = open(os.path.join(os.path.dirname(__file__), 'LICENSE')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='student_locations',
    version='0.5',
    packages=['student_locations'],
    include_package_data=True,
    license=LICENSE,  # example license
    description='A Django app that allows students to add thier location and contact info to a google map',
    long_description=README,
    url='',
    author='Eric Parker',
    author_email='eric_parker@harvard.edu',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        "Django>=1.6",
        "ims_lti_py",
        "lxml",
        "oauth2",
        "requests",
        "django-crispy-forms",
        "django-cached-authentication-middleware>=0.2.0"
        "django-auth-lti",
    ],
    tests_require=[
        'mock',
    ],
    zip_safe=False,
)
