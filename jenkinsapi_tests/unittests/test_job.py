import mock
import unittest
import datetime

from jenkinsapi.job import Job


class TestJob(unittest.TestCase):

    DATA = {"actions": [],
            "description": "test job",
            "displayName": "foo",
            "displayNameOrNull": None,
            "name": "foo",
            "url": "http://halob:8080/job/foo/",
            "buildable": True,
            "builds": [{"number": 3, "url": "http://halob:8080/job/foo/3/"},
           {"number": 2, "url": "http://halob:8080/job/foo/2/"},
                {"number": 1, "url": "http://halob:8080/job/foo/1/"}],
            "color": "blue",
            "firstBuild": {"number": 1, "url": "http://halob:8080/job/foo/1/"},
            "healthReport": [{"description": "Build stability: No recent builds failed.",
                             "iconUrl": "health-80plus.png", "score": 100}],
            "inQueue": False,
            "keepDependencies": False,
            "lastBuild": {"number": 3, "url": "http://halob:8080/job/foo/3/"},
            "lastCompletedBuild": {"number": 3, "url": "http://halob:8080/job/foo/3/"},
            "lastFailedBuild": None,
            "lastStableBuild": {"number": 3, "url": "http://halob:8080/job/foo/3/"},
            "lastSuccessfulBuild": {"number": 3, "url": "http://halob:8080/job/foo/3/"},
            "lastUnstableBuild": None,
            "lastUnsuccessfulBuild": None,
            "nextBuildNumber": 4,
            "property": [],
            "queueItem": None,
            "concurrentBuild": False,
            "downstreamProjects": [],
            "scm": {},
            "upstreamProjects": []}

    @mock.patch.object(Job, '_poll')
    def setUp(self, _poll):
        _poll.return_value = self.DATA

        # def __init__( self, url, name, jenkins_obj ):

        self.J = mock.MagicMock()  # Jenkins object
        self.j = Job('http://halob:8080/job/foo/', 'foo', self.J)

    def testRepr(self):
        # Can we produce a repr string for this object
        repr(self.j)

    def testName(self):
        with self.assertRaises(AttributeError):
        	self.j.id()
    	self.assertEquals(self.j.name, 'foo')

    def test_special_urls(self):
        self.assertEquals(self.j.baseurl, 'http://halob:8080/job/foo')

        self.assertEquals(self.j.get_delete_url(), 'http://halob:8080/job/foo/doDelete')

        self.assertEquals(self.j.get_rename_url(), 'http://halob:8080/job/foo/doRename')

if __name__ == '__main__':
    unittest.main()
