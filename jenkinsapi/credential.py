"""
Module for jenkinsapi Credential class
"""

from jenkinsapi.jenkinsbase import JenkinsBase
import logging

log = logging.getLogger(__name__)


class Credential(JenkinsBase):
    """
    Class to hold information on credentials

    This class doesn't hold any username/password information
    You can create Credential instance with username and password,
    but the those fields will be cleared once credentials are loaded from
    Jenkins
    """
    def __init__(self, username=None, password=None):
        """
        Init a credential object by providing all relevant pointers to it

        :param credential_id: Jenkins internal credential ID
        :param description: as Jenkins doesn't allow human friendly names for credentials
            and makes "displayName" itself, there is no way to find credential later,
            this field is used to distinguish between credentials
        :param fullname: Jenkins internal name,
            like 'credential-store/_/79972988-efd6-49f0-b14e-d341251d8d7b'
        :param typename: Type of the credential
        :return: Credential obj
        """
        self.credential_id = None
        self.description = None
        self.fullname = None
        self.displayname = None
        self.typename = None
        self.username = username
        self.password = password

    def __str__(self):
        return self.description


class UsernamePasswordCredential(Credential):
    def __init__(self, username=None, password=None):
        super(UsernamePasswordCredential, self).__init__(username=username,
                                                         password=password)
