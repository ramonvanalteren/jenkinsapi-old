"""
Important: For this test to work we need at least one Jenkins server
You need to configure the JENKINS_BASE environment variable
And you need to enure that this Jenkins has at least one job called "test1".
Make sure that sucsessful builds of test one archive an artifact called "test1.txt" - it can be anything.
"""
import unittest
import logging

from pyjenkinsci.jenkins import jenkins
from pyjenkinsci.artifact import artifact
from pyjenkinsci.build import build
from pyjenkinsci_tests.config import HTTP_PROXY, JENKINS_BASE

if __name__ == "__main__":
    logging.basicConfig()

log = logging.getLogger(__name__)

class test_query( unittest.TestCase ):
    """
    Perform a number of basic queries.
    """

    def setUp(self):
        log.warn("Connecting to %s via proxy: %s" % (JENKINS_BASE, HTTP_PROXY) )
        self.jenkins = jenkins( JENKINS_BASE )

    def testListJobs(self):
        """
        Test that we can get a list of jobs
        """
        job_ids = self.jenkins.keys()
        assert "test1" in job_ids

    def testListBuilds(self):
        """
        """
        test1 = self.jenkins["test1"]
        builds = [a for a in test1.get_build_ids() ]
        assert len(builds) > 0
        newest_build = test1[ builds[-1] ]
        assert isinstance( newest_build, build )

    def testGetLatestArtifact(self):
        test1 = self.jenkins["test1"]
        builds = [a for a in test1.get_build_ids() ]
        assert len(builds) > 0
        newest_build = test1[ builds[0] ]
        assert isinstance( newest_build, build )
        artifact_dict = newest_build.get_artifact_dict()
        assert "test1.txt" in artifact_dict.keys()
        test_artifact = artifact_dict[ "test1.txt" ]
        assert isinstance( test_artifact, artifact )


if __name__ == "__main__":
    unittest.main()
