"""
Kerberos aware Requester
"""
from jenkinsapi.utils.requester import Requester
from requests_kerberos import HTTPKerberosAuth, OPTIONAL


# pylint: disable=W0222
class KrbRequester(Requester):

    """
    A class which carries out HTTP requests with Kerberos/GSSAPI authentication.
    """

    def __init__(self, ssl_verify=None, baseurl=None, mutual_auth=OPTIONAL):
        """
        :param ssl_verify: flag indicating if server certificate in HTTPS requests should be
                           verified
        :param baseurl: Jenkins' base URL
        :param mutual_auth: type of mutual authentication, use one of REQUIRED, OPTIONAL or DISABLED
                            from requests_kerberos package
        """
        args = {}
        if ssl_verify:
            args["ssl_verify"] = ssl_verify
        if baseurl:
            args["baseurl"] = baseurl
        super(KrbRequester, self).__init__(**args)
        self.mutual_auth = mutual_auth

    def get_request_dict(self, params=None, data=None, files=None, headers=None):
      req_dict = super(KrbRequester, self).get_request_dict(params=params, data=data, files=files,
                                                            headers=headers)
      if self.mutual_auth:
         auth = HTTPKerberosAuth(self.mutual_auth)
      else:
         auth = HTTPKerberosAuth()
      req_dict['auth'] = auth
      return req_dict
