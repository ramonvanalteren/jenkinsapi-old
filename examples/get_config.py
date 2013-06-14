import logging
logging.basicConfig()

from jenkinsapi.jenkins import Jenkins
J = Jenkins('http://localhost:8080')
jobName = 'create_fwrgmkbbzk'

config = J[jobName].get_config()

print config

