import io
import sys
import requests

url = 'http://mirrors.jenkins-ci.org/war/latest/jenkins.war'
print url



response = requests.get(url)
total_length = response.headers.get('content-length')

print total_length

with io.open('jenkins.war', 'wb') as jw:

    for i, data in enumerate(response.iter_content()):
        jw.write(data)

        if i % 1024 == 0:
            sys.stdout.write('.')

