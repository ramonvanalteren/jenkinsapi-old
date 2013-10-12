import logging
from jenkinsapi.job import Job
from jenkinsapi.custom_exceptions import JenkinsAPIException

log = logging.getLogger(__name__)


class Jobs(object):

    def __init__(self, jenkins):
        self.jenkins = jenkins

    def __len__(self):
        return len(self.keys)

    def __delitem__(self, job_name):
        """
        Delete a job by name
        :param job_name: name of a exist job, str
        """
        if job_name in self:
            delete_job_url = self[job_name].get_delete_url()
            self.jenkins.requester.post_and_confirm_status(
                delete_job_url,
                data='some random bytes...'
            )
            self.jenkins.poll()

    def __getitem__(self, job_name):
        for row in self.jenkins._data.get('jobs', []):
            if row['name'] == job_name:
                return Job(
                    row['url'],
                    row['name'],
                    self.jenkins)
        else:
            return None

    def iteritems(self):
        """
        Get the names & objects for all jobs
        """
        self.jenkins.poll()
        for row in self.jenkins._data.get('jobs', []):
            name = row['name']
            url = row['url']

            yield name, Job(url, name, self.jenkins)

    def __contains__(self, job_name):
        """
        True if job_name is the name of a defined job
        """
        return job_name in self.keys()

    def iterkeys(self):
        """
        Get the names of all available views
        """
        for row in self.jenkins._data.get('jobs', []):
            yield row['name']

    def keys(self):
        """
        Return a list of the names of all jobs
        """
        return list(self.iterkeys())

    def create(self, job_name, config):
        """
        Create a job
        :param jobname: name of new job, str
        :param config: configuration of new job, xml
        :return: new Job obj
        """
        if job_name in self:
            return self[job_name]

        params = {'name': job_name}
        if isinstance(config, unicode):
            config = str(config)
        self.jenkins.requester.\
                post_xml_and_confirm_status(self.jenkins.get_create_url(),
                                            data=config, params=params)
        self.jenkins.poll()
        if job_name not in self:
            raise JenkinsAPIException('Cannot create job %s' % job_name)

        return self[job_name]

    def copy(self, job_name, new_job_name):
        """
        Copy a job
        :param job_name: name of a exist job, str
        :param new_job_name: name of new job, str
        :return: new Job obj
        """
        params = {'name': new_job_name,
                  'mode': 'copy',
                  'from': job_name}

        self.jenkins.requester.post_and_confirm_status(
            self.jenkins.get_create_url(),
            params=params,
            data='')
        self.jenkins.poll()
        return self[new_job_name]

    def rename(self, job_name, new_job_name):
        """
        Rename a job
        :param job_name: name of a exist job, str
        :param new_job_name: name of new job, str
        :return: new Job obj
        """
        params = {'newName': new_job_name}
        rename_job_url = self[job_name].get_rename_url()
        self.jenkins.requester.post_and_confirm_status(
            rename_job_url, params=params, data='')
        self.jenkins.poll()
        return self[new_job_name]

    def build(self, job_name, params):
        assert(isinstance(params, dict))
        self[job_name].invoke(build_params=params)
