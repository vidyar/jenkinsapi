from jenkinsapi.api import search_artifacts

jenkinsurl = "http://127.0.0.1:8080/jenkins"
jobid = "test1"
artifact_ids = [ "test1.txt", "test2.txt" ] # I need a build that contains all of these
result = search_artifacts(jenkinsurl, jobid, artifact_ids)
print((repr(result )))
