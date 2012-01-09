from pyhudson.hudson import hudson
from pyhudson.exceptions import ArtifactsMissing
from types import NoneType


def searchArtifacts( hudsonurl, jobid, artifact_ids=[], same_build=True, build_search_limit=None ):
    """
    Search the entire history of a hudson job for a list of artifact names. If same_build
    is true then ensure that all artifacts come from the same build of the job
    """
    if len( artifact_ids ) == 0:
        return []
    
    assert same_build, "same_build==False not supported yet"
    assert isinstance( build_search_limit, ( NoneType, int ))
    
    h = hudson( hudsonurl )        
    j = h[ jobid ] 
    
    build_ids = j.getBuildIds()
    
    firstBuildId = None
    
    for build_id in build_ids:
        build = j.getBuild( build_id )
        
        artifacts = build.getArtifactDict()
        
        if set( artifact_ids ).issubset( set( artifacts.keys() ) ):
            return dict( ( a,artifacts[a] ) for a in artifact_ids )
    
        missing_artifacts =  set( artifact_ids ) - set( artifacts.keys() )
        
        if build_search_limit == None:
            raise ("Artifacts %s missing from %s #%i" % ( ", ".join( missing_artifacts ), jobid, build_id ) )
        else:
            if firstBuildId:
                if firstBuildId - build_id > build_search_limit:
                    raise ( "Artifacts %s missing from %s #%i after search of depth %i " 
                            % ( ", ".join( missing_artifacts ), jobid, build_id, build_search_limit ) )
            else:
                firstBuildId = build_id
                
    raise ArtifactsMissing( missing_artifacts )


def searchForArtifactByRegExp( hudsonurl, jobid, artifactRegExp, same_build=True, build_search_limit=None ): 
    """
    Search the entire history of a hudson job for a list of artifact names. If same_build
    is true then ensure that all artifacts come from the same build of the job
    """
    
    assert same_build, "same_build==False not supported yet"
    
    h = hudson( hudsonurl )
    j = h[ jobid ] 
    
    build_ids = j.getBuildIds()
    
    for build_id in build_ids:
        build = j.getBuild( build_id )
        
        artifacts = build.getArtifactDict()
        
        for name, art in artifacts.iteritems():
            md_match = artifactRegExp.search( name )
            
            if md_match:
                return art
        
    return None