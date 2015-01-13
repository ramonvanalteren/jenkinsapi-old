import pytz
import mock
# To run unittests on python 2.6 please use unittest2 library
try:
    import unittest2 as unittest
except ImportError:
    import unittest
import datetime

from jenkinsapi.build import Build


class test_build(unittest.TestCase):

    DATA = {
        'actions': [{'causes': [{'shortDescription': 'Started by user anonymous',
                                 'userId': None,
                                 'userName': 'anonymous'}]},
                    None,
                    {'causes': []}],
        'artifacts': [],
        'building': False,
        'builtOn': '',
        'changeSet': {'items': [], 'kind': None},
        'culprits': [],
        'description': None,
        "duration": 5782,
        'estimatedDuration': 106,
        'executor': None,
        "fingerprint": [{"fileName": "BuildId.json",
                         "hash": "e3850a45ab64aa34c1aa66e30c1a8977",
                         "original": {"name": "ArtifactGenerateJob",
                                      "number": 469},
                         "timestamp": 1380270162488,
                         "usage": [{"name": "SingleJob",
                                    "ranges": {"ranges": [{"end": 567,
                                                           "start": 566}]}},
                                   {"name": "MultipleJobs",
                                    "ranges": {"ranges": [{"end": 150,
                                                           "start": 139}]}}]
                         }],
        'fullDisplayName': 'foo #1',
        'id': '2013-05-31_23-15-40',
        'keepLog': False,
        'number': 1,
        'result': 'SUCCESS',
        'timestamp': 1370042140000,
        'url': 'http://localhost:8080/job/foo/1/'}

    @mock.patch.object(Build, '_poll')
    def setUp(self, _poll):
        _poll.return_value = self.DATA
        self.j = mock.MagicMock()  # Job
        self.j.name = 'FooJob'

        self.b = Build('http://', 97, self.j)

    def test_timestamp(self):
        self.assertIsInstance(self.b.get_timestamp(), datetime.datetime)

        expected = pytz.utc.localize(
            datetime.datetime(2013, 5, 31, 23, 15, 40))

        self.assertEqual(self.b.get_timestamp(), expected)

    def testName(self):
        with self.assertRaises(AttributeError):
            self.b.id()
        self.assertEquals(self.b.name, 'foo #1')

    def test_duration(self):
        expected = datetime.timedelta(milliseconds=5782)
        self.assertEquals(self.b.get_duration(), expected)
        self.assertEquals(self.b.get_duration().seconds, 5)
        self.assertEquals(self.b.get_duration().microseconds, 782000)
        self.assertEquals(str(self.b.get_duration()), '0:00:05.782000')

    def test_get_causes(self):
        self.assertEquals(self.b.get_causes(),
                          [{'shortDescription': 'Started by user anonymous',
                            'userId': None,
                            'userName': 'anonymous'}])

    @mock.patch.object(Build, 'get_data')
    def test_build_depth(self, get_data_mock):
        Build('http://halob:8080/job/foo/98', 98, self.j, depth=0)
        get_data_mock.assert_called_with('http://halob:8080/job/foo/98/api/'
                                         'python',
                                         tree=None, params={'depth': 0})

    def test_get_revision_no_scm(self):
        """ with no scm, get_revision should return None """
        self.assertEqual(self.b.get_revision(), None)

    ## TEST DISABLED - DOES NOT WORK
    # def test_downstream(self):
    #     expected = ['SingleJob','MultipleJobs']
    #     self.assertEquals(self.b.get_downstream_job_names(), expected)


def main():
    unittest.main(verbosity=2)

if __name__ == '__main__':
    main()
