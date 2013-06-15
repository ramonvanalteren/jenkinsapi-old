'''
System tests for `jenkinsapi.jenkins` module.
'''
import time
import logging
import unittest
from jenkinsapi.jenkins import Jenkins
from jenkinsapi_tests.systests.base import BaseSystemTest

log = logging.getLogger(__name__)


class TestNodes(BaseSystemTest):
    def test_invoke_job_parameterized(self):

        J = Jenkins('http://localhost:8080')
        J.create_node('test')

if __name__ == '__main__':
    logging.basicConfig()
    unittest.main()
