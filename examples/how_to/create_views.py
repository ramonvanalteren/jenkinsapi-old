import logging

from jenkinsapi.view import View
from jenkinsapi.jenkins import Jenkins

log_level = getattr(logging, 'DEBUG')
logging.basicConfig(level=log_level)
logger = logging.getLogger()

jenkins_url = "http://192.168.1.64:8080/"
#jenkins_url = "http://localhost:7080/"

api = Jenkins(jenkins_url)

# Create ListView in main view
logger.info('Attempting to create new view')
test_view_name = 'SimpleListView'
new_view = api.views.create(test_view_name)
logger.info('new_view is %s' % new_view)
if new_view is None:
    logger.error('View was not created')
else:
    logger.info('View has been created')

logger.info('Attempting to create view that already exists')
if not api.views.create(test_view_name):
    logger.info('View was not created')
else:
    logger.error('View has been created')

logger.info('Attempting to delete view that already exists')

del api.views[test_view_name]
if test_view_name in api.views:
    logger.error('View was not deleted')
else:
    logger.info('View has been deleted')

logger.info('Attempting to delete view that does not exist')
del api.views[test_view_name]
if not test_view_name in api.views:
    logger.error('View has been deleted')
else:
    logger.info('View was not deleted')
