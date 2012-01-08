from setuptools import setup, find_packages
import sys, os

# Use the README file as the long-description for the project. 
# This makes sure that the PyPi index page contains automatically
# generated documentation.
PROJECT_ROOT, _ = os.path.split(__file__) 
DESCRIPTION = open( os.path.join(PROJECT_ROOT, "README") ).read()
VERSION = REVISION = '0.1.1'
PROJECT_NAME = 'jenkinsapi'
PROJECT_AUTHORS = "Salim Fadhley, Ramon van Alteren"

GLOBAL_ENTRY_POINTS = {
        "console_scripts":[ "jenkins_invoke=jenkinsapi.command_line.jenkins_invoke:main"]
        }

setup(name=PROJECT_NAME,
      version=VERSION,
      author=PROJECT_AUTHORS,
      author_email='salimfadhley@gmail.com, ramon@vanalteren.nl',
      packages=find_packages('.'),
      zip_safe=True,
      include_package_data = False,
      entry_points = GLOBAL_ENTRY_POINTS,
      url="https://github.com/salimfadhley/jenkinsapi",
      description='A Python API for accessing resources on a Jenkins continuous-integration server.',
      long_description=DESCRIPTION,
      )
