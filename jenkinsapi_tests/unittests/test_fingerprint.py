import mock
# To run unittests on python 2.6 please use unittest2 library
try:
    import unittest2 as unittest
except ImportError:
    import unittest
import hashlib
import requests

from jenkinsapi.jenkins import Jenkins
from jenkinsapi.jenkinsbase import JenkinsBase
from jenkinsapi.fingerprint import Fingerprint
from jenkinsapi.utils.requester import Requester


class TestFingerprint(unittest.TestCase):

    def setUp(self):
        self.baseurl = 'http://localhost:8080'
        m = hashlib.md5()
        m.update("some dummy string".encode('ascii'))
        self.dummy_md5 = m.hexdigest()

    @mock.patch.object(Jenkins, '_poll')
    @mock.patch.object(JenkinsBase, '_poll')
    def test_object_creation(self, _poll, _basepoll):
        J = Jenkins(self.baseurl, username='foouser', password='foopassword')
        self.fp_instance = Fingerprint(self.baseurl, self.dummy_md5, J)
        self.assertTrue(isinstance(self.fp_instance, Fingerprint))
        self.assertEquals(str(self.fp_instance), self.dummy_md5)
        self.assertTrue(self.fp_instance.valid())

    @mock.patch.object(Jenkins, '_poll')
    @mock.patch.object(JenkinsBase, '_poll')
    def test_valid_with_requests_HTTPError_404(self, _poll, _basepoll):
        resp_obj = requests.models.Response()
        resp_obj.status_code = 404
        _poll.side_effect = requests.exceptions.HTTPError(response=resp_obj)
        J = Jenkins(self.baseurl, username='foouser', password='foopassword')
        fp = Fingerprint(self.baseurl, self.dummy_md5, J)
        self.assertTrue(fp.valid())

    @mock.patch.object(Jenkins, '_poll')
    @mock.patch.object(JenkinsBase, '_poll')
    def test_valid_with_requests_HTTPError_Not404(self, _poll, _basepoll):
        resp_obj = requests.models.Response()
        resp_obj.status_code = 401
        _poll.side_effect = requests.exceptions.HTTPError(response=resp_obj)
        J = Jenkins(self.baseurl, username='foouser', password='foopassword')
        fp = Fingerprint(self.baseurl, self.dummy_md5, J)
        self.assertFalse(fp.valid())

if __name__ == '__main__':
    unittest.main()
