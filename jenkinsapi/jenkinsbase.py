import urllib
import urllib2
import logging
import pprint
from jenkinsapi import config
from jenkinsapi.utils.retry import retry_function

log = logging.getLogger(__name__)

class JenkinsBase(object):
    """
    This appears to be the base object that all other jenkins objects are inherited from
    """
    RETRY_ATTEMPTS = 5

    def __repr__(self):
        return """<%s.%s %s>""" % (self.__class__.__module__,
                                   self.__class__.__name__,
                                   str( self ))

    def print_data(self):
        pprint.pprint(self._data)

    def __str__(self):
        raise NotImplemented

    def __init__(self, baseurl, poll=True):
        """
        Initialize a jenkins connection
        """
        self.baseurl = baseurl
        if poll:
            try:
                self.poll()
            except urllib2.HTTPError, hte: #TODO: Wrong exception
                log.exception(hte)
                log.warn( "Failed to connect to %s" % baseurl )
                raise

    def __eq__(self, other):
        """
        Return true if the other object represents a connection to the same server
        """
        if not isinstance(other, self.__class__):
            return False
        if not other.baseurl == self.baseurl:
            return False
        return True

    def poll(self):
        self._data = self._poll()

    def _poll(self):
        url = self.python_api_url(self.baseurl)
        requester = self.get_jenkins_obj().requester
        content = retry_function(self.RETRY_ATTEMPTS , requester.hit_url, url)
        try:
            return eval(content)
        except SyntaxError:
            log.exception('Inappropriate content found at %s' % url)

    @classmethod
    def python_api_url(cls, url):
        if url.endswith(config.JENKINS_API):
            return url
        else:
            if url.endswith(r"/"):
                fmt="%s%s"
            else:
                fmt = "%s/%s"
            return fmt % (url, config.JENKINS_API)