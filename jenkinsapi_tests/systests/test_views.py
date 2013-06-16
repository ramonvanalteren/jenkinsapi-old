'''
System tests for `jenkinsapi.jenkins` module.
'''
import logging
import unittest
from jenkinsapi.view import View
from jenkinsapi_tests.systests.base import BaseSystemTest
from jenkinsapi_tests.test_utils.random_strings import random_string

log = logging.getLogger(__name__)


class TestViews(BaseSystemTest):
    def test_make_views(self):
        self._create_job()
        view_name = random_string()
        self.assertNotIn(view_name, self.jenkins.views())
        v = self.jenkins.views().create(view_name)
        self.assertIn(view_name, self.jenkins.views())
        self.assertIsInstance(v, View)

if __name__ == '__main__':
    logging.basicConfig()
    unittest.main()
