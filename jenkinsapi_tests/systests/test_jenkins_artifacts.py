'''
System tests for `jenkinsapi.jenkins` module.
'''
import os
import time
import shutil
import tempfile
import unittest

from jenkinsapi_tests.systests.base import BaseSystemTest
from jenkinsapi_tests.systests.job_configs import JOB_WITH_ARTIFACTS
from jenkinsapi_tests.test_utils.random_strings import random_string

class TestPingerJob(BaseSystemTest):

    def test_invoke_job(self):
        job_name = 'create_%s' % random_string()
        job = self.jenkins.create_job(job_name, JOB_WITH_ARTIFACTS)
        job.invoke(block=True)

        b = job.get_last_build()

        while b.is_running():
            time.sleep(0.25)

        artifacts = b.get_artifact_dict()
        self.assertIsInstance(artifacts, dict)

        artifact = artifacts['out.txt']

        tempDir = tempfile.mkdtemp()

        try:
            artifact.save_to_dir(tempDir)
            readBackText = open(os.path.join(tempDir, artifact.filename), 'rb').read().strip()
            self.assertTrue(readBackText.startswith('PING localhost'))
            self.assertTrue(readBackText.endswith('ms'))
        finally:
            shutil.rmtree(tempDir)

if __name__ == '__main__':
    unittest.main()
