from jenkinsapi.api import search_artifact_by_regexp
import re

jenkinsurl = "http://127.0.0.1:8080/jenkins"
jobid = "test1"
artifact_regexp = re.compile("test1\.txt") # A file name I want.
result = search_artifact_by_regexp(jenkinsurl, jobid, artifact_regexp)
print((repr(result)))
