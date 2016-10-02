from __future__ import print_function

from jenkinsapi.api import search_artifact_by_regexp
import re

jenkinsurl = "http://localhost:8080"
jobid = "foo"
artifact_regexp = re.compile("test1\.txt")  # A file name I want.
result = search_artifact_by_regexp(jenkinsurl, jobid, artifact_regexp)
print((repr(result)))
