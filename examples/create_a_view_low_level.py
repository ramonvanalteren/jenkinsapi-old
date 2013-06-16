"""
A low level example:
This is how JenkinsAPI creates views
"""
import requests
import json

url = 'http://localhost:8080/newView'
str_view_name = "ddsfddfd"
params = {}# {'name': str_view_name}
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
data = {
    "mode": "hudson.model.ListView",
    #"Submit": "OK",
    "name": str_view_name
}
# Try 1
result = requests.post(url, params=params, data={'json':json.dumps(data)}, headers=headers)
print result.text.encode('UTF-8')
