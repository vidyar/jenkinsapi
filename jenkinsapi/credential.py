"""
Module for jenkinsapi Credential class
"""

from jenkinsapi.jenkinsbase import JenkinsBase
import logging

log = logging.getLogger(__name__)


class Credential(JenkinsBase):
    """
    Class to hold information on credential defined in Jenkins
    """

    GLOBAL = 'GLOBAL'
    SYSTEM = 'SYSTEM'

    def __init__(self, url, username, jenkins_obj):
        self.username = username
        self.jenkins_obj = jenkins_obj
        super(Credential, self).__init__(baseurl=url)

    def get_jenkins_obj(self):
        return self.jenkins_obj
