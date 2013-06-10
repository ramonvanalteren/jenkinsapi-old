'''
System tests for `jenkinsapi.jenkins` module.
'''
import time
import unittest
from jenkinsapi_tests.test_utils.random_strings import random_string
from jenkinsapi_tests.systests.base import BaseSystemTest

PINGER_JOB_CONFIG = """
<?xml version='1.0' encoding='UTF-8'?>
<project>
  <actions/>
  <description>Ping a load of stuff for about 10s</description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <scm class="hudson.scm.NullSCM"/>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers class="vector"/>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>ping -c 5 localhost | tee out.txt</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers>
    <hudson.tasks.ArtifactArchiver>
      <artifacts>*.txt</artifacts>
      <latestOnly>false</latestOnly>
    </hudson.tasks.ArtifactArchiver>
  </publishers>
  <buildWrappers/>
</project>""".strip()

class TestPingerJob(BaseSystemTest):

    def test_invoke_job(self):
        job_name = 'create_%s' % random_string()
        job = self.jenkins.create_job(job_name, PINGER_JOB_CONFIG)
        job.invoke(block=True)

        b = job.get_last_build()

        while b.is_running():
            time.sleep(0.25)

        artifacts = b.get_artifact_dict()
        self.assertIsInstance(artifacts, dict)

        outfile = artifacts['out.txt']

        # TODO: Actually verify the download


if __name__ == '__main__':
    unittest.main()
