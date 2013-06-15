'''
System tests for `jenkinsapi.jenkins` module.
'''
import time
import logging
import unittest
from jenkinsapi.jenkins import Jenkins
from jenkinsapi_tests.systests.base import BaseSystemTest
from jenkinsapi_tests.test_utils.random_strings import random_string

log = logging.getLogger(__name__)


class TestNodes(BaseSystemTest):
    def test_invoke_job_parameterized(self):
        node_name = random_string()
        J = Jenkins('http://localhost:8080')
        J.create_node(node_name)
        self.assertTrue(J.has_node(node_name))

        N = J.get_node(node_name)
        self.assertEquals(N.baseurl, J.get_node_url(node_name))

        J.delete_node(node_name)
        self.assertFalse(J.has_node(node_name))

if __name__ == '__main__':
    logging.basicConfig()
    unittest.main()
