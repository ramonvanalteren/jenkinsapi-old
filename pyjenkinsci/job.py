import logging
import urlparse
import urllib2
from datetime import time
from pyjenkinsci.build import Build
from pyjenkinsci.jenkinsbase import JenkinsBase

from exceptions import NoBuildData, NotFound

log = logging.getLogger(__name__)

class Job(JenkinsBase):
    """
    Represents a jenkins job
    A job can hold N builds which are the actual execution environments
    """
    def __init__( self, url, name, jenkins_obj ):
        self.name = name
        self.jenkins = jenkins_obj
        JenkinsBase.__init__( self, url )

    def id( self ):
        return self._data["name"]

    def __str__(self):
        return self._data["name"]

    def get_jenkins_obj(self):
        return self.jenkins

    def get_build_triggerurl( self, token=None ):
        if token is None:
            extra = "build"
        else:
            assert isinstance(token, str ), "token if provided should be a string."
            extra = "build?token=%s" % token
        buildurl = urlparse.urljoin( self.baseurl, extra )
        return buildurl

    def hit_url(self, url ):
        fn_urlopen = self.get_jenkins_obj().get_opener()
        try:
            stream = fn_urlopen( url )
            html_result = stream.read()
        except urllib2.HTTPError, e:
            log.debug( "Error reading %s" % url )
            raise
        return html_result

    def invoke( self, securitytoken=None, block=False, skip_if_running=False, invoke_pre_check_delay=3, invoke_block_delay=15 ):
        assert isinstance( invoke_pre_check_delay, (int, float) )
        assert isinstance( invoke_block_delay, (int, float) )
        assert isinstance( block, bool )
        assert isinstance( skip_if_running, bool )
        skip_build = False
        if self.is_queued():
            log.warn( "Will not request new build because %s is already queued" % self.id() )
            skip_build = True
        elif self.is_running():
            if skip_if_running:
                log.warn( "Will not request new build because %s is already running" % self.id() )
                skip_build = True
            else:
                log.warn("Will re-schedule %s even though it is already running" % self.id() )
        original_build_no = self.get_last_buildnumber()
        if skip_build:
            pass
        else:
            log.info( "Attempting to start %s on %s" % ( self.id(), repr(self.get_jenkins_obj()) ) )
            url = self.get_build_triggerurl( securitytoken )
            html_result = self.hit_url( url )
            assert len( html_result ) > 0
        if invoke_pre_check_delay > 0:
            log.info("Waiting for %is to allow Hudson to catch up" % invoke_pre_check_delay )
            time.sleep( invoke_pre_check_delay )
        if block:
            total_wait = 0
            while self.is_queued():
                log.info( "Waited %is for %s to begin..." % ( total_wait, self.id() ) )
                time.sleep( invoke_block_delay )
                total_wait += invoke_block_delay
            if self.is_running():
                running_build = self.get_last_build()
                running_build.block_until_complete( delay=invoke_pre_check_delay )
                assert running_build.is_good()
            else:
                assert self.get_last_buildnumber() > original_build_no, "Job does not appear to have run."
        else:
            if self.is_queued():
                log.info( "%s has been queued." % self.id() )
            elif self.is_running():
                log.info( "%s is running." % self.id() )
            elif original_build_no < self.get_last_buildnumber():
                log.info( "%s has completed." % self.id() )
            else:
                raise AssertionError("The job did not schedule.")

    def _buildid_for_type(self, buildtype):
        """Gets a buildid for a given type of build"""
        KNOWNBUILDTYPES=["lastSuccessfulBuild", "lastBuild", "lastCompletedBuild"]
        assert buildtype in KNOWNBUILDTYPES
        buildid = self._data[buildtype]["number"]
        assert type(buildid) == int, "Build ID should be an integer, got %s" % repr( buildid )
        return buildid

    def get_last_good_buildnumber( self ):
        """
        Get the numerical ID of the last good build.
        """
        return self._buildid_for_type(buildtype="lastSuccessfulBuild")

    def get_last_buildnumber( self ):
        """
        Get the numerical ID of the last build.
        """
        return self._buildid_for_type(buildtype="lastBuild")

    def get_last_completed_buildnumber( self ):
        """
        Get the numerical ID of the last complete build.
        """
        return self._buildid_for_type(buildtype="lastCompletedBuild")

    def get_build_dict(self):
        if not self._data.has_key( "builds" ):
            raise NoBuildData( repr(self) )
        return dict( ( a["number"], a["url"] ) for a in self._data["builds"] )

    def get_revision_dict(self):
        """
        Get dictionary of all revision:buildnumber available
        """
        if not self._data.has_key( "builds" ):
            raise NoBuildData( repr(self) )
        return dict( ( self.get_build(a["number"] ).get_revision(), a["number"] ) for a in self._data["builds"] ) 

    def get_build_ids(self):
        """
        Return a sorted list of all good builds as ints.
        """
        return reversed( sorted( self.get_build_dict().keys() ) )

    def get_last_good_build( self ):
        """
        Get the last good build
        """
        bn = self.get_last_good_buildnumber()
        return self.get_build( bn )

    def get_last_build( self ):
        """
        Get the last good build
        """
        bn = self.get_last_buildnumber()
        return self.get_build( bn )

    def get_last_completed_build( self ):
        """
        Get the last build regardless of status
        """
        bn = self.get_last_completed_buildnumber()
        return self.get_build( bn )

    def get_buildnumber_for_revision(self, revision ):
        """
        Returns the buildnumber for a revision
        """
        if not isinstance(revision, int):
            revision = int(revision)
        revmap = self.get_revision_dict()
        try:
            return revmap[revision]
        except KeyError:
            raise NotFound("Couldn't find a build with that revision")

    def get_build( self, buildnumber ):
        assert type(buildnumber) == int
        url = self.get_build_dict()[ buildnumber ]
        return Build( url, buildnumber, job=self )

    def __getitem__( self, buildnumber ):
        return self.get_build(buildnumber)

    def is_queued_or_running(self):
        return self.is_queued() or self.is_running()

    def is_queued(self):
        self.poll()
        return self._data["inQueue"]

    def is_running(self):
        self.poll()
        try:
            return self.get_last_build().is_running()
        except NoBuildData:
            log.info("No build info available for %s, assuming not running." % str(self) )
            return False
