"""
Module for jenkinsapi folders
"""

import copy
import logging
from jenkinsapi.node import Folder
from jenkinsapi.jobs import Jobs
from jenkinsapi.custom_exceptions import UnknownFolder

log = logging.getLogger(__name__)


class Folders(Jobs):
    """
    Class to hold a collection of folders
    """

    def __init__(self, jenkins_obj):
        """
        Handy access to nodes
        """
        self.jenkins = jenkins_obj
        # We replace poll method to filter out jobs and leave only folders
        self.original_poll = jenkins_obj.poll
        self.jenkins.poll = self.poll

    def poll(self):
        '''
        Special poll method which removes all non-folders
        from Jenkins API json
        '''
        url = self.jenkins.python_api_url(self.jenkins.baseurl)
        self._data = self.jenkins.get_data(url)
        if self._data.get('jobs') is not None:
            jobs = self._data['jobs']
            only_folders = [folder for folder in jobs if folder.get('color')]
            self._data['jobs'] = only_folders

    def get_jenkins_obj(self):
        '''
        Returns copy of Jenkins object with original poll() method
        '''
        jenkins = copy.deepcopy(self.jenkins)
        jenkins.poll = self.original_poll
        return jenkins

    def __str__(self):
        return 'Folders @ %s' % self.jenkins.baseurl

    def __contains__(self, folder_name):
        return folder_name in self.keys()

    def iterkeys(self):
        for item in self._data['jobs']:
            if not item.get('color'):
                yield item['name']

    def keys(self):
        return list(self.iterkeys())

    def iteritems(self):
        for item in self._data['jobs']:
            foldername = item['name']
            folderurl = '%s/job/%s' % (self.baseurl, foldername)
            yield item['name'], Folder(folderurl,
                                       foldername, self.jenkins)

    def __getitem__(self, foldername):
        self_as_dict = dict(self.iteritems())
        if foldername in self_as_dict:
            return self_as_dict[foldername]
        else:
            raise UnknownFolder(foldername)

    def __len__(self):
        return len(self.iteritems())
