"""
Start a Parameterized Build
"""
from __future__ import print_function

from jenkinsapi.jenkins import Jenkins

J = Jenkins('http://localhost:8080')

params = {'VERSION': '1.2.3', 'PYTHON_VER': '2.7'}

J.build_job('foo', params)
