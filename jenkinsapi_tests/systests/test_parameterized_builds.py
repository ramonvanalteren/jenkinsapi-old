'''
System tests for `jenkinsapi.jenkins` module.
'''
import time
# To run unittests on python 2.6 please use unittest2 library
try:
    import unittest2 as unittest
except ImportError:
    import unittest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from jenkinsapi_tests.systests.base import BaseSystemTest
from jenkinsapi_tests.test_utils.random_strings import random_string
from jenkinsapi_tests.systests.job_configs import JOB_WITH_FILE
from jenkinsapi_tests.systests.job_configs import JOB_WITH_FILE_AND_PARAMS
from jenkinsapi_tests.systests.job_configs import JOB_WITH_PARAMETERS
from jenkinsapi.custom_exceptions import WillNotBuild


class TestParameterizedBuilds(BaseSystemTest):

    def test_invoke_job_with_file(self):
        file_data = random_string()
        param_file = StringIO(file_data)

        job_name = 'create_%s' % random_string()
        job = self.jenkins.create_job(job_name, JOB_WITH_FILE)
        job.invoke(block=True, files={'file.txt': param_file})

        build = job.get_last_build()
        while build.is_running():
            time.sleep(0.25)

        artifacts = build.get_artifact_dict()
        self.assertIsInstance(artifacts, dict)
        art_file = artifacts['file.txt']
        self.assertTrue(art_file.get_data().strip(), file_data)

    def test_invoke_job_parameterized(self):
        param_B = random_string()

        job_name = 'create_%s' % random_string()
        job = self.jenkins.create_job(job_name, JOB_WITH_PARAMETERS)
        job.invoke(block=True, build_params={'B': param_B})

        build = job.get_last_build()
        while build.is_running():
            time.sleep(0.25)

        artifacts = build.get_artifact_dict()
        self.assertIsInstance(artifacts, dict)
        artB = artifacts['b.txt']
        self.assertTrue(artB.get_data().strip(), param_B)

        self.assertIn(param_B, build.get_console())

    def test_parameterized_job_build_queuing(self):
        """Accept multiple builds of parameterized jobs with unique
           parameters."""
        job_name = 'create_%s' % random_string()
        job = self.jenkins.create_job(job_name, JOB_WITH_PARAMETERS)

        for i in range(3):
            param_B = random_string()
            params = {'B': param_B}
            job.invoke(build_params=params)
            time.sleep(0.25)

        self.assertTrue(job.has_queued_build(params))

        while job.has_queued_build(params):
            time.sleep(0.25)

        build = job.get_last_build()
        while build.is_running():
            time.sleep(0.25)

        artifacts = build.get_artifact_dict()
        self.assertIsInstance(artifacts, dict)
        artB = artifacts['b.txt']
        self.assertTrue(artB.get_data().strip(), param_B)

        self.assertIn(param_B, build.get_console())

    def test_parameterized_job_build_rejection(self):
        """Reject build of paramterized job when existing build with same
           parameters is queued, raising WillNotBuild."""
        job_name = 'create_%s' % random_string()
        job = self.jenkins.create_job(job_name, JOB_WITH_PARAMETERS)

        for i in range(3):
            params = {'B': random_string()}
            job.invoke(build_params=params)

        with self.assertRaises(WillNotBuild) as na:
            job.invoke(build_params=params)
        expected_msg = 'A build with these parameters is already queued.'
        self.assertEqual(str(na.exception), expected_msg)

    def test_invoke_job_with_file_and_params(self):
        file_data = random_string()
        param_data = random_string()
        param_file = StringIO(file_data)

        job_name = 'create_%s' % random_string()
        job = self.jenkins.create_job(job_name, JOB_WITH_FILE_AND_PARAMS)
        job.invoke(block=True, files={'file.txt': param_file},
                   build_params={'B': param_data})

        build = job.get_last_build()
        while build.is_running():
            time.sleep(0.25)

        artifacts = build.get_artifact_dict()
        self.assertIsInstance(artifacts, dict)
        art_file = artifacts['file.txt']
        self.assertTrue(art_file.get_data().strip(), file_data)
        art_param = artifacts['file1.txt']
        self.assertTrue(art_param.get_data().strip(), param_data)


if __name__ == '__main__':
    unittest.main()
