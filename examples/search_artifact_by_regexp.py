from jenkinsapi.api import search_artifact_by_regexp
import logging
import re

jenkinsurl = "http://localhost:8080/jenkins"
jobid = "test1"
artifactRegExp = re.compile( "test1\.txt" ) # A file name I want.

result = search_artifact_by_regexp( jenkinsurl, jobid, artifactRegExp )

print repr( result )