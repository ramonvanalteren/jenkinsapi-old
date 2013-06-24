'''
System tests for `jenkinsapi.jenkins` module.
'''
import unittest
from jenkinsapi.build import Build
from jenkinsapi.invocation import Invocation
from jenkinsapi_tests.systests.base import BaseSystemTest
from jenkinsapi_tests.test_utils.random_strings import random_string
from jenkinsapi_tests.systests.job_configs import LONG_RUNNING_JOB, SHORTISH_JOB


class TestInvocation(BaseSystemTest):

    def test_invocation_object(self):
        job_name = 'create_%s' % random_string()
        job = self.jenkins.create_job(job_name, LONG_RUNNING_JOB)
        ii = job.invoke()
        self.assertIsInstance(ii, Invocation)
        self.assertTrue(ii.is_queued_or_running())
        self.assertEquals(ii.get_build_number(), 1)

    def test_get_block_until_build_running(self):
        job_name = 'create_%s' % random_string()
        job = self.jenkins.create_job(job_name, LONG_RUNNING_JOB)
        ii = job.invoke()
        bn = ii.get_build_number()
        self.assertIsInstance(bn, int)
        ii.block(until='not_queued')
        self.assertTrue(ii.is_running())
        b = ii.get_build()
        self.assertIsInstance(b, Build)
        ii.stop()
        self.assertFalse(ii.is_running())

    def test_get_block_until_build_complete(self):
        job_name = 'create_%s' % random_string()
        job = self.jenkins.create_job(job_name, SHORTISH_JOB)
        ii = job.invoke()
        ii.block(until='completed')
        self.assertFalse(ii.is_running())

if __name__ == '__main__':
    unittest.main()
