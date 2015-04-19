import mock
# To run unittests on python 2.6 please use unittest2 library
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import jenkinsapi
from jenkinsapi import config
from jenkinsapi.job import Job
from jenkinsapi.jenkinsbase import JenkinsBase
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.custom_exceptions import NoBuildData


class TestJob(unittest.TestCase):
    JOB_DATA = {'actions': [None, {}],
                'buildable': True,
                'builds': [{'number': 106,
                            'url': 'http://dlsysadm-ap72:18080/jenkins/job/ecd-webgoat/106/'},
                           {'number': 105,
                            'url': 'http://dlsysadm-ap72:18080/jenkins/job/ecd-webgoat/105/'},
                           {'number': 104,
                            'url': 'http://dlsysadm-ap72:18080/jenkins/job/ecd-webgoat/104/'},
                           {'number': 103,
                            'url': 'http://dlsysadm-ap72:18080/jenkins/job/ecd-webgoat/103/'},
                           {'number': 102,
                            'url': 'http://dlsysadm-ap72:18080/jenkins/job/ecd-webgoat/102/'},
                           {'number': 101,
                            'url': 'http://dlsysadm-ap72:18080/jenkins/job/ecd-webgoat/101/'},
                           {'number': 100,
                            'url': 'http://dlsysadm-ap72:18080/jenkins/job/ecd-webgoat/100/'},
                           {'number': 99,
                            'url': 'http://dlsysadm-ap72:18080/jenkins/job/ecd-webgoat/99/'},
                           {'number': 98,
                            'url': 'http://dlsysadm-ap72:18080/jenkins/job/ecd-webgoat/98/'},
                           {'number': 97,
                            'url': 'http://dlsysadm-ap72:18080/jenkins/job/ecd-webgoat/97/'}],
                'color': 'red',
                'concurrentBuild': False,
                'description': '',
                'displayName': 'ecd-webgoat',
                'displayNameOrNull': None,
                'downstreamProjects': [],
                'firstBuild': {'number': 97,
                               'url': 'http://dlsysadm-ap72:18080/jenkins/job/ecd-webgoat/97/'},
                'healthReport': [{'description': 'Build stability: 1 out of the last 5 builds failed.',
                                  'iconUrl': 'health-60to79.png',
                                  'score': 80}],
                'inQueue': False,
                'keepDependencies': False,
                'lastBuild': {'number': 106,
                              'url': 'http://dlsysadm-ap72:18080/jenkins/job/ecd-webgoat/106/'},
                'lastCompletedBuild': {'number': 106,
                                       'url': 'http://dlsysadm-ap72:18080/jenkins/job/ecd-webgoat/106/'},
                'lastFailedBuild': {'number': 106,
                                    'url': 'http://dlsysadm-ap72:18080/jenkins/job/ecd-webgoat/106/'},
                'lastStableBuild': {'number': 105,
                                    'url': 'http://dlsysadm-ap72:18080/jenkins/job/ecd-webgoat/105/'},
                'lastSuccessfulBuild': {'number': 105,
                                        'url': 'http://dlsysadm-ap72:18080/jenkins/job/ecd-webgoat/105/'},
                'lastUnstableBuild': None,
                'lastUnsuccessfulBuild': {'number': 106,
                                          'url': 'http://dlsysadm-ap72:18080/jenkins/job/ecd-webgoat/106/'},
                'modules': [{'color': 'blue',
                             'displayName': 'webgoat',
                             'name': 'com.googlecode:webgoat',
                             'url': 'http://dlsysadm-ap72:18080/jenkins/job/ecd-webgoat/com.googlecode$webgoat/'}],
                'name': 'ecd-webgoat',
                'nextBuildNumber': 107,
                'property': [{}],
                'queueItem': None,
                'scm': {},
                'upstreamProjects': [],
                'url': 'http://dlsysadm-ap72:18080/jenkins/job/ecd-webgoat/'
                }

    URL_DATA = {'http://halob:8080/job/foo/%s' % config.JENKINS_API: JOB_DATA}

    def fakeGetData(self, url, **args):
        try:
            return TestJob.URL_DATA[url]
        except KeyError:
            raise Exception("Missing data for %s" % url)

#     def fake_add_missing_builds(self, data):
#         return data

    @mock.patch.object(JenkinsBase, 'get_data', fakeGetData)
    #@mock.patch.object(Job, '_add_missing_builds', fake_add_missing_builds)
    def setUp(self):

        self.J = mock.MagicMock()  # Jenkins object
        self.j = Job('http://halob:8080/job/foo/', 'foo', self.J)

    @mock.patch.object(JenkinsBase, 'get_data', fakeGetData)
    def test_get_last_good_buildnumber(self):
        ret = self.j.get_last_good_buildnumber()
        self.assertTrue(ret, 3)

    @mock.patch.object(JenkinsBase, 'get_data', fakeGetData)
    def test_has_params(self):
        self.assertFalse(self.j.has_params())


if __name__ == '__main__':
    unittest.main()
