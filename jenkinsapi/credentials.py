"""
This module implements the Credentials class, which is intended to be a
container-like interface for all of the Global credentials defined on a single
Jenkins node.
"""
import logging
import urllib
from jenkinsapi.credential import Credential
from jenkinsapi.credential import UsernamePasswordCredential
from jenkinsapi.jenkinsbase import JenkinsBase
from jenkinsapi.custom_exceptions import JenkinsAPIException

log = logging.getLogger(__name__)


class Credentials(JenkinsBase):
    """
    This class provides a container-like API which gives
    access to all global credentials on a Jenkins node.

    Returns a list of Credential Objects.
    """
    def __init__(self, baseurl, jenkins_obj):
        self.baseurl = baseurl
        self.jenkins = jenkins_obj
        JenkinsBase.__init__(self, baseurl)

        self.credentials = self._data['credentials']

    def _poll(self, tree=None):
        url = self.python_api_url(self.baseurl)
        data = self.get_data(url, tree=tree)
        credentials = data['credentials']
        for cred_id in credentials.keys():
            cred_url = self.python_api_url('%s/credential/%s' % (self.baseurl, cred_id))
            cred_dict = self.get_data(cred_url)

            cr = None
            if cred_dict['typeName'] == 'Username with password':
                cr = UsernamePasswordCredential(None, None)
            else:
                cr = Credential(None, None)

            cr.credential_id = cred_id
            cr.description = cred_dict['description']
            cr.fullname = cred_dict['fullName']
            cr.typename = cred_dict['typeName']
            cr.displayname = cred_dict['displayName']
            credentials[cred_id] = cr

        return data

    def __str__(self):
        return 'Global Credentials @ %s' % self.baseurl

    def get_jenkins_obj(self):
        return self.jenkins

    def __iter__(self):
        for cred in self.credentials.itervalues():
            yield cred.description

    def __contains__(self, description):
        return description in self.keys()

    def iterkeys(self):
        return self.__iter__()

    def keys(self):
        return list(self.iterkeys())

    def iteritems(self):
        for cred in self.credentials.itervalues():
            yield cred.description, cred

    def __getitem__(self, description):
        for cred in self.credentials.itervalues():
            if cred.description == description:
                return cred

        raise KeyError('Credential with description "%s" not found'
                        % description)

    def __len__(self):
        return len(self.keys())

    def __setitem__(self, description, credential):
        """
        Creates Credential in Jenkins using username, password and description
        Description must be unique in Jenkins instance
        because it is used to find Credential later.

        If description already exists - this method is going to update existing Credential

        :param str description: Credential description
        :param tuple credential_tuple: (username, password, description) tuple.
        """
        if description not in self:
            if isinstance(credential, UsernamePasswordCredential):
                params = {
                    # 'stapler-class': 'com.cloudbees.plugins.credentials.impl.CertificateCredentialsImpl',
                    # '_.id': '',
                    # 'keyStoreSource': '0',
                    # '_.keyStoreFile': '',
                    # 'stapler-class': 'com.cloudbees.plugins.credentials.impl.CertificateCredentialsImpl%24FileOnMasterKeyStoreSource',
                    # '_.uploadedKeystore': ' ',
                    # 'stapler-class': 'com.cloudbees.plugins.credentials.impl.CertificateCredentialsImpl%24UploadedKeyStoreSource',
                    # '_.password': ' ',
                    # '_.description': ' ',
                    # 'stapler-class': 'com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPassword',
                    # '_.id': ' ',
                    # '_.username': username,
                    # '_.password': password,
                    # '_.description': description,
                    # 'stapler-class': 'com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey',
                    'stapler-class': 'com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl',
                    'Submit': 'OK',
                    'json': {
                        "": "1",
                        "credentials": {
                            "stapler-class": "com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl",
                            "id": "",
                            "username": credential.username,
                            "password": credential.password,
                            "description": description
                        }}
                    }
            url = '%s/credential-store/domain/_/createCredentials' % self.jenkins.baseurl
        else:
            # update existing credentials
            cred = self[description]
            if isinstance(cred, UsernamePasswordCredential):
                params = {
                    'stapler-class': 'com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl',
                    '_.id': cred.credential_id,
                    '_.username': cred.username,
                    '_.password': cred.password,
                    '_.description': description,
                    'json': {
                        "stapler-class": "com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl",
                        "id": cred.credential_id,
                        "username": cred.username,
                        "password": cred.password,
                        "description": description
                    },
                    'Submit': 'Save'
                }
            url = '%s/credential-store/domain/_/credential/%s/updateSubmit' \
                % (self.jenkins.baseurl, cred.credential_id)

        try:
            self.jenkins.requester.post_and_confirm_status(url, params={}, data=urllib.urlencode(params))
        except HTTPError:
            raise JenkinsAPIException('Latest version of Credentials '
                                      'plugin is required to be able '
                                      'to create/update credentials')
        self.poll()
        self.credentials = self._data['credentials']
        if description not in self:
            raise JenkinsAPIException('Problem creating/updating credential.')

    def get(self, item, default):
        return self[item] if item in self else default

    def __delitem__(self, description):
        params = {
            'Submit': 'OK',
            'json': {}
        }
        url = ('%s/credential-store/domain/_/credential/%s/doDelete'
               % (self.jenkins.baseurl, self[description].credential_id))
        try:
            self.jenkins.requester.post_and_confirm_status(url, params={}, data=urllib.urlencode(params))
        except HTTPError:
            raise JenkinsAPIException('Latest version of Credentials '
                                      'required to be able to create '
                                      'credentials')
        self.poll()
        self.credentials = self._data['credentials']
        if description in self:
            raise JenkinsAPIException('Problem deleting credential.')
