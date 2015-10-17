'''
System tests for `jenkinsapi.jenkins` module.
'''

from jenkinsapi_tests.systests.base import BaseSystemTest
from jenkinsapi_tests.systests.job_configs import LONG_RUNNING_JOB
from jenkinsapi_tests.test_utils.random_strings import random_string
import logging
import time
# To run unittests on python 2.6 please use unittest2 library
try:
    import unittest2 as unittest
except ImportError:
    import unittest


log = logging.getLogger(__name__)


class TestNodes(BaseSystemTest):

    def test_get_executors(self):
        node_name = random_string()
        node_dict = {
            'num_executors': 2,
            'node_description': 'Test JNLP Node',
            'remote_fs': '/tmp',
            'labels': 'systest_jnlp',
            'exclusive': True
        }
        self.jenkins.nodes.create_node(node_name, node_dict)
        executors = self.jenkins.get_executors(node_name)
        self.assertEqual(executors.count, 2)
        for count, execs in enumerate(executors):
            self.assertEqual(count, execs.get_number())
            self.assertEqual(execs.is_idle(), True)

    def test_running_executor(self):
        node_name = random_string()
        node_dict = {
            'num_executors': 1,
            'node_description': 'Test JNLP Node',
            'remote_fs': '/tmp',
            'labels': 'systest_jnlp',
            'exclusive': True
        }
        self.jenkins.nodes.create_node(node_name, node_dict)
        job_name = 'create_%s' % random_string()
        job = self.jenkins.create_job(job_name, LONG_RUNNING_JOB)
        qq = job.invoke()
        qq.block_until_building()

        if job.is_running() is False:
            time.sleep(1)
        executors = self.jenkins.get_executors(node_name)
        all_idle = True
        for execs in executors:
            if execs.is_idle() is False:
                all_idle = False
                self.assertNotEqual(execs.get_progress(), -1)
                self.assertEqual(
                    execs.get_current_executable(),
                    qq.get_build_number())
                self.assertEqual(execs.likely_stuck(), False)
        self.assertEqual(
            all_idle,
            True,
            "Executor should have been triggered.")

    def test_idle_executors(self):
        node_name = random_string()
        node_dict = {
            'num_executors': 1,
            'node_description': 'Test JNLP Node',
            'remote_fs': '/tmp',
            'labels': 'systest_jnlp',
            'exclusive': True
        }
        self.jenkins.nodes.create_node(node_name, node_dict)
        executors = self.jenkins.get_executors(node_name)

        for execs in executors:
            self.assertEqual(execs.get_progress(), -1)
            self.assertEqual(execs.get_current_executable(), None)
            self.assertEqual(execs.likely_stuck(), False)
            self.assertEqual(execs.is_idle(), True)


if __name__ == '__main__':
    logging.basicConfig()
    unittest.main()
