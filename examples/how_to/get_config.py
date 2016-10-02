"""
An example of how to use JenkinsAPI to fetch the config XML of a job.
"""
from __future__ import print_function

from jenkinsapi.jenkins import Jenkins
J = Jenkins('http://localhost:8080')
jobName = J.keys()[0]  # Just get the first job

config = J[jobName].get_config()

print(config)
