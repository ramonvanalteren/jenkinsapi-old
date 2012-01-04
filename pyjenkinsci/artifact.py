import urllib2
import os
import logging
import cStringIO
import zipfile
import cPickle
import datetime
import hashlib
from pyjenkinsci import config

from pyjenkinsci.utils.retry import retry_function
from pyjenkinsci.exceptions import ArtifactBroken

log = logging.getLogger( __name__ )

class Artifact(object):

    @staticmethod
    def timedelta_to_seconds( td ):
        secs = float( td.seconds )
        secs += td.microseconds / 1000000.0
        secs += td.days * 86400
        return secs

    def __init__( self, filename, url, build=None ):
        self.filename = filename
        self.url = url
        self.build = build

    def unpickle(self, method="pickle" ):
        """
        Assume that the object is a pickled stream.
        """
        stream, _ = retry_function(  config.LOAD_ATTEMPTS , self.getstream )

        while True:
            try:
                yield cPickle.load( stream )
            except EOFError:
                break

    def logging_buffer_copy( self, input_stream, output_stream, length, chunks=10 ):

        chunk_points = int( length / chunks )

        start_time = datetime.datetime.now()
        last_time = datetime.datetime.now()

        for index in xrange( 0, length ):
            output_stream.write( input_stream.read(1) )

            if chunk_points > 0:
                if ( index % chunk_points ) == 0 and ( index > 0 ):
                    now = datetime.datetime.now()

                    try:
                        time_elapsed_since_start = self.timedelta_to_seconds( now - start_time )
                        # avg_bitrate = ( index / time_elapsed_since_start ) / 1024.0
                        time_elapsed_since_last_chunk = self.timedelta_to_seconds( now - last_time )
                        inst_bitrate = ( chunk_points / time_elapsed_since_last_chunk ) / 1024.0
                    except ZeroDivisionError, _:
                        continue

                    log.info( "Loaded %i of %i bytes %.2f kbit/s" % ( index, length, inst_bitrate ) )
                    last_time = now


    def getstream( self ):
        """
        Get the artifact as a stream
        """
        artifact_digest = hashlib.md5()
        tmp_buffer = cStringIO.StringIO()

        if self.build:
            fn_opener = self.build.job.hudson.get_opener()
        else:
            fn_opener = urllib2.urlopen

        try:
            inputstream = fn_opener( self.url, )
            content_type = inputstream.info().get("content-type", "unknown")

            try:
                content_length = int( inputstream.info()["content-length"] )
                self.logging_buffer_copy( inputstream, tmp_buffer, content_length )
            except KeyError, ke:
                # Could not get length.
                log.warn("Could not get length")
                tmp_buffer.write( inputstream.read() )

        except urllib2.HTTPError:
            log.warn( "Error fetching %s" % self.url )
            raise
        tmp_buffer.seek(0)

        artifact_digest.update(tmp_buffer.getvalue())
        artifact_hexdigest = artifact_digest.hexdigest()

        artifact_size = len(tmp_buffer.getvalue())
        log.info( "Got %s,  %i bytes, MD5: %s, type: %s" % ( self.filename, artifact_size, artifact_hexdigest, content_type ) )

        if self.build:
            self.build.job.hudson.validate_fingerprint( artifact_hexdigest )

        return tmp_buffer, artifact_hexdigest

    def openzip( self ):
        """
        Open the artifact as a zipfile.
        """
        buffer, _ = retry_function(  config.LOAD_ATTEMPTS , self.getstream )
        zf = zipfile.ZipFile( buffer, "r" )
        return zf

    def save( self, fspath ):
        """
        Save the artifact to an explicit path. The containing directory must exist.
        Returns a reference to the file which has just been writen to.
        """

        log.info( "Saving artifact @ %s to %s" % (self.url, fspath) )

        if not fspath.endswith( self.filename ):
            log.warn( "Attempt to change the filename of artifact %s on save." % self.filename )

        if os.path.exists( fspath ):
            existing_hexdigest = self.get_local_digest( fspath )
            if self.build:
                try:
                    valid = self.build.job.hudson.validate_fingerprint_for_build( existing_hexdigest, filename=self.filename, job=self.build.job.id(), build=self.build.id() )

                    if valid:
                        log.info( "Local copy of %s is already up to date. MD5 %s" % (self.filename, existing_hexdigest) )
                    else:
                        self.__do_download( fspath )
                except ArtifactBroken, ab: #@UnusedVariable
                    log.info("Hudson artifact could not be identified.")
            else:
                log.info("This file did not originate from Hudson, so cannot check.")
                self.__do_download( fspath )
        else:
            log.info("Local file is missing, downloading new.")
            self.__do_download( fspath )

    def get_local_digest( self, fspath ):
        tmp_buffer_existing = cStringIO.StringIO()
        existingfile = open( fspath, "rb" )
        tmp_buffer_existing.write( existingfile.read() )
        existing_digest = hashlib.md5()
        existing_digest.update(tmp_buffer_existing.getvalue())
        existing_hexdigest = existing_digest.hexdigest()
        return existing_hexdigest

    def __do_download( self, fspath ):

        filedir, _ = os.path.split( fspath )
        if not os.path.exists( filedir ):
            log.warn( "Making missing directory %s" % filedir )
            os.makedirs( filedir )

        try:
            outputfile = open( fspath, "wb" )
        except IOError, ioe:
            log.critical("User %s@%s cannot open file" % ( os.environ.get("USERNAME","unknown"),os.environ.get("USERDOMAIN","unknown") )  )
            raise

        tmp_buffer_downloaded, artifact_hexdigest = retry_function( config.LOAD_ATTEMPTS , self.getstream )

        outputfile.write( tmp_buffer_downloaded.getvalue() )
        return outputfile


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
