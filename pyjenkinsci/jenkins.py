import fingerprint
import jenkinsobject
import job
from exceptions import UnknownJob
from utils.urlopener import mkurlopener
import logging
import time
import view

log = logging.getLogger(__name__)

class jenkins(jenkinsobject):
    """
    Represents a jenkins environment.
    """
    def __init__(self, baseurl, proxyhost=None, proxyport=None, proxyuser=None, proxypass=None):
        self.proxyhost = proxyhost
        self.proxyport = proxyport
        self.proxyuser = proxyuser
        self.proxypass = proxypass
        jenkinsobject.__init__( self, baseurl )

    def get_proxy_auth(self):
        return (self.proxyhost, self.proxyport, self.proxyuser, self.proxypass)

    def get_opener( self ):
        return mkurlopener(*self.get_proxy_auth())

    def validate_fingerprint( self, id ):
        obj_fingerprint = fingerprint(self.baseurl, id, jenkins_obj=self)
        obj_fingerprint.validate()
        log.info("Jenkins says %s is valid" % id)

    def get_artifact_data(self, id):
        obj_fingerprint = fingerprint(self.baseurl, id, jenkins_obj=self)
        obj_fingerprint.validate()
        return obj_fingerprint.get_info()

    def validate_fingerprint_for_build(self, digest, filename, job, build ):
        obj_fingerprint = fingerprint( self.baseurl, digest, jenkins_obj=self )
        return obj_fingerprint.validate_for_build( filename, job, build )

    def get_jenkins_obj(self):
        return self

    def get_jobs(self):
        """
        Fetch all the build-names on this Hudson server.
        """
        for info in self._data["jobs"]:
            yield info["name"], job( info["url"], info["name"], jenkins_obj=self)

    def iteritems(self):
        return self.get_jobs()

    def iterkeys(self):
        for info in self._data["jobs"]:
            yield info["name"]

    def keys(self):
        return [ a for a in self.iterkeys() ]

    def __str__(self):
        return "Jenkins server at %s" % self.baseurl

    def _get_views( self ):
        if not self._data.has_key( "views" ):
            pass
        else:
            for viewdict in self._data["views"]:
                yield viewdict["name"], viewdict["url"]

    def get_view_dict(self):
        return dict( self._get_views() )

    def get_view_url( self, str_view_name ):
        try:
            view_dict = self.get_view_dict()
            return view_dict[ str_view_name ]
        except KeyError, ke:
            all_views = ", ".join( view_dict.keys() )
            raise KeyError("View %s is not known - available: %s" % ( str_view_name, all_views ) )

    def get_view(self, str_view_name ):
        view_url = self.get_view_url( str_view_name )
        view_api_url = self.python_api_url( view_url )
        return view(view_api_url , str_view_name, jenkins_obj=self)

    def __getitem__( self, buildname ):
        """
        Get a build
        """
        for name, job in self.get_jobs():
            if name == buildname:
                return job
        raise UnknownJob(buildname)
