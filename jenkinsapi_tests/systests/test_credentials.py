'''
System tests for `jenkinsapi.jenkins` module.
'''
import logging
# To run unittests on python 2.6 please use unittest2 library
try:
    import unittest2 as unittest
except ImportError:
    import unittest
from jenkinsapi_tests.systests.base import BaseSystemTest
from jenkinsapi_tests.test_utils.random_strings import random_string
from jenkinsapi.credentials import Credentials
from jenkinsapi.credential import UsernamePasswordCredential

log = logging.getLogger(__name__)


class TestCredentials(BaseSystemTest):
    def test_get_credentials(self):
        creds = self.jenkins.get_credentials()
        self.assertIsInstance(creds, Credentials)

    def test_delete_inexistant_credential(self):
        with self.assertRaises(KeyError) as ke:
            creds = self.jenkins.get_credentials()

            del creds[random_string()]

    def test_create_credential(self):
        creds = self.jenkins.get_credentials()

        cred_descr = random_string()
        creds[cred_descr] = UsernamePasswordCredential('username', 'password')

        self.assertTrue(cred_descr in creds)
        cred = creds[cred_descr]
        self.assertIsInstance(cred, UsernamePasswordCredential)
        self.assertEquals(cred.password, None)
        self.assertEquals(cred.description, cred_descr)

    def test_delete_credential(self):
        creds = self.jenkins.get_credentials()

        cred_descr = random_string()
        creds[cred_descr] = UsernamePasswordCredential('username', 'password')

        del creds[cred_descr]

    def test_update_credential(self):
        creds = self.jenkins.get_credentials()

        cred_descr = random_string()
        creds[cred_descr] = UsernamePasswordCredential('username', 'password')

        cred = creds[cred_descr]
        cred.username = 'anotheruser'
        cred.password = 'password'

        creds[cred_descr] = cred

        self.assertIn('anotheruser', creds[cred_descr].displayname)


if __name__ == '__main__':
    logging.basicConfig()
    unittest.main()
