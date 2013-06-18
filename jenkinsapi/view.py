from jenkinsapi.jenkinsbase import JenkinsBase
from jenkinsapi.job import Job
import logging
import urllib

log = logging.getLogger(__name__)

class View(JenkinsBase):

    def __init__(self, url, name, jenkins_obj):
        self.name = name
        self.jenkins_obj = jenkins_obj
        JenkinsBase.__init__(self, url)
        self.deleted = False

    def __str__(self):
        return self.name

    def __getitem__(self, job_name):
        assert isinstance(job_name, str)
        api_url = self.python_api_url(self.get_job_url(job_name))
        return Job(api_url, job_name, self.jenkins_obj)

    def delete(self):
        """
        Remove this view object
        """
        url = "%s/doDelete" % self.baseurl
        self.jenkins_obj.requester.post_and_confirm_status(url, data='')
        self.jenkins_obj.poll()
        self.deleted = True

    def keys(self):
        return self.get_job_dict().keys()

    def iteritems(self):
        for name, url in self.get_job_dict().iteritems():
            api_url = self.python_api_url( url )
            yield name, Job(api_url, name, self.jenkins_obj)

    def values(self):
        return [job_row[1] for job_row in self.iteritems()]

    def items(self):
        return [job_row for job_row in self.iteritems() ]

    def _get_jobs( self ):
        for viewdict in self._data.get("jobs"):
            yield viewdict["name"], viewdict["url"]

    def get_job_dict(self):
        return dict(self._get_jobs())

    def __len__(self):
        return len(self.get_job_dict().keys())

    def get_job_url(self, job_name):
        try:
            job_dict = self.get_job_dict()
            return job_dict[job_name]
        except KeyError:
            #noinspection PyUnboundLocalVariable
            all_views = ", ".join( job_dict.keys() )
            raise KeyError("Job %s is not known - available: %s" % ( job_name, all_views ) )

    def get_jenkins_obj(self):
        return self.jenkins_obj

    def add_job(self, job_name, job=None):
        """
        Add job to a view

        :param job_name: name of the job to be added
        :param job: Job object to be added
        :return: True if job has been added, False if job already exists or
         job not known to Jenkins
        """
        if not job:
            if job_name in self.get_job_dict():
                log.error('Job %s is already in the view %s' %
                        (job_name, self.name))
                return False
            elif not self.get_jenkins_obj().has_job(job_name):
                log.error('Job "%s" is not known to Jenkins' % job_name)
                return False

            job = self.jenkins_obj.get_job(job_name)

        jobs = self._data.setdefault('jobs', [])
        jobs.append({'name': job.name, 'url': job.baseurl})
        data = {
            "description":"",
            "statusFilter":"",
            "useincluderegex":"on",
            "includeRegex":"",
            "columns": [{"stapler-class": "hudson.views.StatusColumn",
                        "kind": "hudson.views.StatusColumn"},
                        {"stapler-class": "hudson.views.WeatherColumn",
                        "kind": "hudson.views.WeatherColumn"},
                        {"stapler-class": "hudson.views.JobColumn",
                        "kind": "hudson.views.JobColumn"},
                        {"stapler-class": "hudson.views.LastSuccessColumn",
                        "kind": "hudson.views.LastSuccessColumn"},
                        {"stapler-class": "hudson.views.LastFailureColumn",
                        "kind": "hudson.views.LastFailureColumn"},
                        {"stapler-class": "hudson.views.LastDurationColumn",
                        "kind": "hudson.views.LastDurationColumn"},
                        {"stapler-class": "hudson.views.BuildButtonColumn",
                        "kind": "hudson.views.BuildButtonColumn"}],
            "Submit":"OK",
            }
        data["name"] = self.name
        for job_name in self.get_job_dict().keys():
            data[job_name]='on'
        data['json'] = data.copy()
        self.post_data('%sconfigSubmit' % self.baseurl, urllib.urlencode(data))
        log.debug('Job "%s" has been added to a view "%s"' %
                     (job.name, self.name))
        return True

    def _get_nested_views(self):
        for viewdict in self._data.get("views"):
            yield viewdict["name"], viewdict["url"]

    def get_nested_view_dict(self):
        return dict(self._get_nested_views())
