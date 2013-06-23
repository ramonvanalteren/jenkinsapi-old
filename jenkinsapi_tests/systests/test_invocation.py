'''
System tests for `jenkinsapi.jenkins` module.
'''
import unittest
from jenkinsapi.invocation import Invocation
from jenkinsapi_tests.systests.job_configs import LONG_RUNNING_JOB
from jenkinsapi_tests.test_utils.random_strings import random_string
from jenkinsapi_tests.systests.base import BaseSystemTest


class TestInvocation(BaseSystemTest):

    def test_invocation_object(self):
        job_name = 'create_%s' % random_string()
        job = self.jenkins.create_job(job_name, LONG_RUNNING_JOB)
        ii = job.invoke()
        self.assertIsInstance(ii, Invocation)
        self.assertTrue(ii.is_queued_or_running())
        self.assertEquals(ii.get_build_number(), 1)


    def test_multiple_inocations(self):
    	pass
        


if __name__ == '__main__':
    unittest.main()
