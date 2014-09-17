from mock import Mock, MagicMock, patch, call, mock_open
# To run unittests on python 2.6 please use unittest2 library
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import re, jenkinsapi
from jenkinsapi.artifact import Artifact
from jenkinsapi.build import Build
from jenkinsapi.custom_exceptions import ArtifactBroken

class ArtifactTest(unittest.TestCase):

    def setUp(self):
        self._build = build = Mock()
        build.buildno = 9999
        job = self._build.job
        job.jenkins.baseurl = 'http://localhost'
        job.name = 'TestJob'
        self._artifact = Artifact('artifact.zip', 'http://localhost/job/TestJob/9999/artifact/artifact.zip', build)

    @patch('jenkinsapi.artifact.os.path.exists', spec=True, return_value=True)
    @patch('jenkinsapi.artifact.os.path.isdir', spec=True, return_value=True)
    def test_save_to_dir(self, mock_isdir, mock_exists):
        artifact = self._artifact
        artifact.save = Mock(spec=Artifact.save, return_value='/tmp/artifact.zip')

        self.assertEqual(artifact.save_to_dir('/tmp'), '/tmp/artifact.zip')

        mock_exists.assert_called_once_with('/tmp')
        mock_isdir.assert_called_once_with('/tmp')
        artifact.save.assert_called_once_with('/tmp/artifact.zip', False)

    @patch('jenkinsapi.artifact.os.path.exists', spec=True, return_value=True)
    @patch('jenkinsapi.artifact.os.path.isdir', spec=True, return_value=True)
    def test_save_to_dir_strict(self, mock_isdir, mock_exists):
        artifact = self._artifact
        artifact.save = Mock(return_value='/tmp/artifact.zip')

        self.assertEqual(artifact.save_to_dir('/tmp', strict_validation=True), '/tmp/artifact.zip')

        mock_exists.assert_called_once_with('/tmp')
        mock_isdir.assert_called_once_with('/tmp')
        artifact.save.assert_called_once_with('/tmp/artifact.zip', True)

    @patch('jenkinsapi.artifact.open', mock_open(), create=True)
    @patch('jenkinsapi.artifact.Fingerprint', spec=True)
    def test_verify_download_valid_positive(self, MockFingerprint):
        # mock_open() only mocks out f.read(), which reads all content at a time.
        # However, _verify_download() reads the file in chunks.
        f = jenkinsapi.artifact.open.return_value
        f.read.side_effect = [b'chunk1', b'chunk2', b''] # empty string indicates EOF

        fp = MockFingerprint.return_value
        fp.validate_for_build.return_value = True
        fp.unknown = False

        self.assertTrue(self._artifact._verify_download('/tmp/artifact.zip', False))

        MockFingerprint.assert_called_once_with(
            'http://localhost',
            '097c42989a9e5d9dcced7b35ec4b0486', # MD5 of 'chunk1chunk2'
            self._build.job.jenkins)
        fp.validate_for_build.assert_called_once_with('artifact.zip', 'TestJob', 9999)

    @patch('jenkinsapi.artifact.Fingerprint', spec=True)
    def test_verify_download_valid_negative(self, MockFingerprint):
        artifact = self._artifact
        artifact._md5sum = Mock(return_value='097c42989a9e5d9dcced7b35ec4b0486')

        fp = MockFingerprint.return_value
        fp.validate_for_build.return_value = True
        fp.unknown = True # negative

        self.assertTrue(self._artifact._verify_download('/tmp/artifact.zip', False)) # not strict

    @patch('jenkinsapi.artifact.Fingerprint', spec=True)
    def test_verify_download_valid_negative_strict(self, MockFingerprint):
        artifact = self._artifact
        artifact._md5sum = Mock(return_value='097c42989a9e5d9dcced7b35ec4b0486')

        fp = MockFingerprint.return_value
        fp.validate_for_build.return_value = True
        fp.unknown = True # negative

        with self.assertRaisesRegexp(ArtifactBroken, re.escape(
                'Artifact 097c42989a9e5d9dcced7b35ec4b0486 seems to be broken, check http://localhost')):
            self._artifact._verify_download('/tmp/artifact.zip', True) # strict

    @patch('jenkinsapi.artifact.open', mock_open(), create=True)
    @patch('jenkinsapi.artifact.Fingerprint', spec=True)
    def test_verify_download_invalid(self, MockFingerprint):
        f = jenkinsapi.artifact.open.return_value
        f.read.side_effect = [b'chunk1', b'chunk2', b''] # empty string indicates EOF

        fp = MockFingerprint.return_value
        fp.validate_for_build.return_value = False
        fp.unknown = False

        with self.assertRaisesRegexp(ArtifactBroken, re.escape(
                'Artifact 097c42989a9e5d9dcced7b35ec4b0486 seems to be broken, check http://localhost')):
            self._artifact._verify_download('/tmp/artifact.zip', False)

        MockFingerprint.assert_called_once_with(
            'http://localhost',
            '097c42989a9e5d9dcced7b35ec4b0486', # MD5 of 'chunk1chunk2'
            self._build.job.jenkins)
        fp.validate_for_build.assert_called_once_with('artifact.zip', 'TestJob', 9999)

    @patch('jenkinsapi.artifact.os.path.exists', spec=True, return_value=True)
    def test_save_has_valid_local_copy(self, mock_exists):
        artifact = self._artifact
        artifact._verify_download = Mock(return_value=True)

        self.assertEqual(artifact.save('/tmp/artifact.zip'), '/tmp/artifact.zip')

        mock_exists.assert_called_once_with('/tmp/artifact.zip')
        artifact._verify_download.assert_called_once_with('/tmp/artifact.zip', False)

    @patch('jenkinsapi.artifact.os.path.exists', spec=True, return_value=True)
    def test_save_has_invalid_local_copy_download_again(self, mock_exists):
        artifact = self._artifact
        artifact._verify_download = Mock(side_effect=[ArtifactBroken, True])
        artifact._do_download = Mock(return_value='/tmp/artifact.zip')

        self.assertEqual(artifact.save('/tmp/artifact.zip', True), '/tmp/artifact.zip')

        mock_exists.assert_called_once_with('/tmp/artifact.zip')
        artifact._do_download.assert_called_once_with('/tmp/artifact.zip')
        self.assertEqual(artifact._verify_download.mock_calls, [call('/tmp/artifact.zip', True)] * 2)

    @patch('jenkinsapi.artifact.os.path.exists', spec=True, return_value=True)
    def test_save_has_invalid_local_copy_download_but_invalid(self, mock_exists):
        artifact = self._artifact
        artifact._verify_download = Mock(side_effect=[ArtifactBroken, ArtifactBroken])
        artifact._do_download = Mock(return_value='/tmp/artifact.zip')

        with self.assertRaises(ArtifactBroken):
            artifact.save('/tmp/artifact.zip', True)

        mock_exists.assert_called_once_with('/tmp/artifact.zip')
        artifact._do_download.assert_called_once_with('/tmp/artifact.zip')
        self.assertEqual(artifact._verify_download.mock_calls, [call('/tmp/artifact.zip', True)] * 2)

    @patch('jenkinsapi.artifact.os.path.exists', spec=True, return_value=False)
    def test_save_has_no_local_copy(self, mock_exists):
        artifact = self._artifact
        artifact._do_download = Mock(return_value='/tmp/artifact.zip')
        artifact._verify_download = Mock(return_value=True)

        self.assertEqual(artifact.save('/tmp/artifact.zip'), '/tmp/artifact.zip')

        mock_exists.assert_called_once_with('/tmp/artifact.zip')
        artifact._do_download.assert_called_once_with('/tmp/artifact.zip')
        artifact._verify_download.assert_called_once_with('/tmp/artifact.zip', False)

