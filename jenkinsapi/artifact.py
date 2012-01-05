from __future__ import with_statement
import urllib
import os
import logging
import hashlib

from jenkinsapi.exceptions import ArtifactBroken
from jenkinsapi.fingerprint import Fingerprint

log = logging.getLogger( __name__ )

class Artifact(object):

    def __init__( self, filename, url, build=None ):
        self.filename = filename
        self.url = url
        self.build = build

    def save( self, fspath ):
        """
        Save the artifact to an explicit path. The containing directory must exist.
        Returns a reference to the file which has just been writen to.

        :param fspath: full pathname including the filename, str
        :return: filepath
        """
        log.info( "Saving artifact @ %s to %s" % (self.url, fspath) )
        if not fspath.endswith( self.filename ):
            log.warn( "Attempt to change the filename of artifact %s on save." % self.filename )
        if os.path.exists(fspath):
            if self.build:
                try:
                    if self._verify_download(fspath):
                        log.info( "Local copy of %s is already up to date." % self.filename)
                        return fspath
                except ArtifactBroken:
                    log.info("Jenkins artifact could not be identified.")
            else:
                log.info("This file did not originate from Jenkins, so cannot check.")
        else:
            log.info("Local file is missing, downloading new.")
        filename = self._do_download(fspath)
        try:
            self._verify_download(filename)
        except ArtifactBroken:
            log.warning("fingerprint of the downloaded artifact could not be verified")
        return filename

    def _do_download(self, fspath):
        filename, headers = urllib.urlretrieve(self.url, filename=fspath)
        return filename

    def _verify_download(self, fspath):
        local_md5 = self._md5sum(fspath)
        fp = Fingerprint(self.build.job.jenkins.baseurl, local_md5, self.build.job.jenkins)
        return fp.validate_for_build(fspath, self.build.job, self.build)

    def _md5sum(self, fspath, chunksize=2**20):
        md5 = hashlib.md5()
        try:
            with open(fspath,'rb') as f:
                for chunk in iter(lambda: f.read(chunksize), ''):
                     md5.update(chunk)
        except:
            raise
        return md5.hexdigest()

    def savetodir( self, dirpath ):
        """
        Save the artifact to a folder. The containing directory must be exist, but use the artifact's
        default filename.
        """
        assert os.path.exists( dirpath )
        assert os.path.isdir( dirpath )
        outputfilepath = os.path.join( dirpath, self.filename )
        self.save( outputfilepath )


    def __repr__( self ):
        return """<%s.%s %s>""" % ( self.__class__.__module__,
                                    self.__class__.__name__,
                                    self.url )
