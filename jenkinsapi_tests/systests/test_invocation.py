'''
System tests for `jenkinsapi.jenkins` module.
'''
import unittest
from jenkinsapi.invocation import Invocation
from jenkinsapi_tests.test_utils.random_strings import random_string
from jenkinsapi_tests.systests.base import BaseSystemTest, EMPTY_JOB_CONFIG


class TestInvocation(BaseSystemTest):

    def test_invocation_object(self):
        job_name = 'create_%s' % random_string()
        job = self.jenkins.create_job(job_name, EMPTY_JOB_CONFIG)
        ii = job.invoke()
        self.assertIsInstance(ii, Invocation)




if __name__ == '__main__':
    unittest.main()
