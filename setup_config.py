from setuptools import setup, find_packages
import sys, os

# Use the README file as the long-description for the project. 
# This makes sure that the PyPi index page contains automatically
# generated documentation.
PROJECT_ROOT, _ = os.path.split(__file__) 
DESCRIPTION = open( os.path.join(PROJECT_ROOT, "README") ).read()
VERSION = REVISION = '0.1.1'
PROJECT_NAME = 'JenkinsAPI'
PROJECT_AUTHORS = "Salim Fadhley, Ramon van Alteren, Ruslan Lutsenko"
PROJECT_EMAILS = 'salimfadhley@gmail.com, ramon@vanalteren.nl, ruslan.lutcenko@gmail.com'
PROJECT_URL = "https://github.com/salimfadhley/jenkinsapi"
SHORT_DESCRIPTION = 'A Python API for accessing resources on a Jenkins continuous-integration server.'

GLOBAL_ENTRY_POINTS = {
        "console_scripts":[ "jenkins_invoke=jenkinsapi.command_line.jenkins_invoke:main"]
        }

if __name__ == "__main__":
    print(DESCRIPTION)