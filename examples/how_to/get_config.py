"""
An example of how to use JenkinsAPI to fetch the config XML of a job.
"""
from jenkinsapi.jenkins import Jenkins
J = Jenkins('http://127.0.0.1:8080')
jobName = 'create_fwrgmkbbzk'

config = J[jobName].get_config()

print config

