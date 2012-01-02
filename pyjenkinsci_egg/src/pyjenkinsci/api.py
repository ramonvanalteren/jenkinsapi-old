from pyjenkinsci.jenkins import jenkins
from pyjenkinsci.artifact import artifact
from pyjenkinsci.exceptions import ArtifactsMissing, TimeOut, BadURL
from pyjenkinsci import constants
from urllib2 import urlparse

import os
import time
import logging

log = logging.getLogger(__name__)

def get_latest_test_results( jenkinsurl, jobname ):
    """
    A convenience function to fetch down the very latest test results from a jenkins job.
    """
    latestbuild = get_latest_build( jenkinsurl, jobname )
    res = latestbuild.get_resultset()
    return res

def get_latest_build( jenkinsurl, jobname ):
    """
    A convenience function to fetch down the very latest test results from a jenkins job.
    """
    jenkinsci = jenkins( jenkinsurl )
    job = jenkinsci[ jobname ]
    return job.get_last_build()

def get_latest_complete_build( jenkinsurl, jobname ):
    """
    A convenience function to fetch down the very latest test results from a jenkins job.
    """
    jenkinsci = jenkins( jenkinsurl )
    job = jenkinsci[ jobname ]
    return job.get_last_completed_build()

def get_artifacts( jenkinsurl, jobid=None, build_no=None, proxyhost=None, proxyport=None, proxyuser=None, proxypass=None ):
    """
    Find all the artifacts for the latest build of a job.
    """
    jenkinsci = jenkins( jenkinsurl, proxyhost, proxyport, proxyuser, proxypass )
    job = jenkinsci[ jobid ]
    if build_no:
        build = job.get_build( build_no )
    else:
        build = job.get_last_good_build()
    artifacts = dict( (artifact.filename, artifact) for artifact in build.get_artifacts() )
    log.info("Found %i artifacts in '%s'" % ( len(artifacts.keys() ), build_no ) )
    return artifacts

def search_artifacts(jenkinsurl, jobid, artifact_ids=None, same_build=True, build_search_limit=None):
    """
    Search the entire history of a jenkins job for a list of artifact names. If same_build
    is true then ensure that all artifacts come from the same build of the job
    """
    if len( artifact_ids ) == 0 or artifact_ids is None:
        return []
    assert same_build, "same_build==False not supported yet"
    jenkinsci = jenkins( jenkinsurl )
    job = jenkinsci[ jobid ]
    build_ids = job.get_build_ids()
    for build_id in build_ids:
        build = job.get_build( build_id )
        artifacts = build.get_artifact_dict()
        if set( artifact_ids ).issubset( set( artifacts.keys() ) ):
            return dict( ( a,artifacts[a] ) for a in artifact_ids )
        missing_artifacts =  set( artifact_ids ) - set( artifacts.keys() )
        log.debug("Artifacts %s missing from %s #%i" % ( ", ".join( missing_artifacts ), jobid, build_id ))
    raise ArtifactsMissing( missing_artifacts )

def grab_artifact( jenkinsurl, jobid, artifactid, targetdir ):
    """
    Convenience method to find the latest good version of an artifact and save it
    to a target directory. Directory is made automatically if not exists.
    """
    artifacts = get_artifacts( jenkinsurl, jobid )
    artifact = artifacts[ artifactid ]
    if not os.path.exists( targetdir ):
        os.makedirs( targetdir )
    artifact.savetodir( targetdir)

def block_until_complete( jenkinsurl, jobs, maxwait=12000, interval=30, raise_on_timeout=True ):
    """
    Wait until all of the jobs in the list are complete.
    """
    assert maxwait > 0
    assert maxwait > interval
    assert interval > 0

    obj_jenkins = jenkins( jenkinsurl )
    obj_jobs = [ obj_jenkins[ jid ] for jid in jobs ]
    for time_left in xrange( maxwait, 0, -interval ):
        still_running = [ j for j in obj_jobs if j.is_queued_or_running() ]
        if not still_running:
            return
        str_still_running = ", ".join( '"%s"' % str(a) for a in still_running )
        log.warn( "Waiting for jobs %s to complete. Will wait another %is" % ( str_still_running, time_left ) )
        time.sleep( interval )
    if raise_on_timeout:
        raise TimeOut( "Waited too long for these jobs to complete: %s" % str_still_running )

def get_view_from_url( url ):
    """
    Factory method
    """
    matched = constants.RE_SPLIT_VIEW_URL.search(url)
    if not matched:
        raise BadURL("Cannot parse URL %s" % url )
    jenkinsurl, view_name = matched.groups()
    jenkinsci = jenkins( jenkinsurl )
    return jenkinsci.get_view( view_name )

def install_artifacts( artifacts, dirstruct, installdir, basestaticurl ):
        """
        Install the artifacts.
        """
        assert basestaticurl.endswith("/"), "Basestaticurl should end with /"
        installed = []
        for reldir, artifactnames in dirstruct.items():
            destdir = os.path.join( installdir, reldir )
            if not os.path.exists( destdir ):
                log.warn( "Making install directory %s" % destdir )
                os.makedirs( destdir )
            else:
                assert os.path.isdir( destdir )
            for artifactname in artifactnames:
                destpath = os.path.abspath( os.path.join( destdir, artifactname ) )
                if artifactname in artifacts.keys():
                    # The artifact must be loaded from jenkins
                    theartifact = artifacts[ artifactname ]
                else:
                    # It's probably a static file, we can get it from the static collection
                    staticurl = urlparse.urljoin( basestaticurl, artifactname )
                    theartifact = artifact( artifactname, staticurl )
                theartifact.save( destpath )
                installed.append( destpath )
        return installed
