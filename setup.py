from setuptools import setup, find_packages
import sys, os

# Use the README file as the long-description for the project. 
# This makes sure that the PyPi index page contains automatically
# generated documentation.
PROJECT_ROOT, _ = os.path.split(sys.argv[0]) 
DESCRIPTION = open( os.path.join(PROJECT_ROOT, "README") ).read()

GLOBAL_ENTRY_POINTS = {
        "console_scripts":[ "jenkins_invoke=jenkinsapi.command_line.jenkins_invoke:main"]
        }

setup(name='jenkinsapi',
      version='0.1',
      author="Salim Fadhley, Ramon van Alteren",
      author_email='salimfadhley@gmail.com, ramon@vanalteren.nl',
      packages=find_packages('.'),
      zip_safe=True,
      include_package_data = False,
      entry_points = GLOBAL_ENTRY_POINTS,
      url="https://github.com/salimfadhley/jenkinsapi",
      description='A Python API for accessing resources on a Jenkins continuous-integration server.',
      long_description=DESCRIPTION,
      )
