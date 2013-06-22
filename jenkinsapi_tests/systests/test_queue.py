'''
System tests for `jenkinsapi.jenkins` module.
'''
import time
import logging
import unittest
from jenkinsapi.queue import Queue
from jenkinsapi.exceptions import NoBuildData
from jenkinsapi_tests.systests.base import BaseSystemTest
from jenkinsapi_tests.test_utils.random_strings import random_string

log = logging.getLogger(__name__)

JOB_XML = """
<?xml version='1.0' encoding='UTF-8'?>
<project>
  <actions/>
  <description></description>
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
      <command>ping -c 200 localhost</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers/>
  <buildWrappers/>
</project>""".strip()


class TestQueue(BaseSystemTest):
    """
    All kinds of testing on Jenkins Queues
    """

    def test_get_queue(self):
        qq = self.jenkins.get_queue()
        self.assertIsInstance(qq, Queue)

    def test_invoke_many_job(self):
        job_names = [random_string() for _ in range(5)]
        jobs = []

        for job_name in job_names:
            j = self.jenkins.create_job(job_name, JOB_XML)
            jobs.append(j)
            j.invoke()

            self.assertTrue(j.is_queued_or_running())

        queue = self.jenkins.get_queue()
        reprString = repr(queue)
        self.assertIn(queue.baseurl, reprString)

    def test_start_and_stop_long_running_job(self):
        job_name = random_string()
        j = self.jenkins.create_job(job_name, JOB_XML)
        j.invoke()
        self.assertTrue(j.is_queued_or_running())

        while j.is_queued():
            time.sleep(0.5)

        j.get_first_build().stop()
        self.assertFalse(j.is_queued_or_running())


if __name__ == '__main__':
    logging.basicConfig()
    unittest.main()
