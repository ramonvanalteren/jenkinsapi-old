#! /bin/bash
virtualenv .
source bin/activate
python setup.py develop
easy_install nose
easy_install mock
easy_install requests
easy_install coverage
nosetests jenkinsapi_tests --with-xunit --with-coverage --cover-html --cover-html-dir=$WORKSPACE/coverage_report --cover-package=jenkinsapi
