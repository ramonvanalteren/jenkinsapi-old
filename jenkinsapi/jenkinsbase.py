"""
Module for JenkinsBase class
"""

import ast
import pprint
import logging
from jenkinsapi import config
from jenkinsapi.custom_exceptions import JenkinsAPIException


class JenkinsBase(object):

    """
    This appears to be the base object that all other jenkins objects are inherited from
    """
    RETRY_ATTEMPTS = 1

    def __repr__(self):
        return """<%s.%s %s>""" % (self.__class__.__module__,
                                   self.__class__.__name__,
                                   str(self))

    def __str__(self):
        raise NotImplementedError

    def __init__(self, baseurl, poll=True):
        """
        Initialize a jenkins connection
        """
        self._data = None
        self.baseurl = self.strip_trailing_slash(baseurl)
        if poll:
            self.poll()

    def get_jenkins_obj(self):
        raise NotImplementedError(
            'Please implement this method on %s' % self.__class__.__name__)

    def __eq__(self, other):
        """
        Return true if the other object represents a connection to the same server
        """
        if not isinstance(other, self.__class__):
            return False
        if not other.baseurl == self.baseurl:
            return False
        return True

    @classmethod
    def strip_trailing_slash(cls, url):
        while url.endswith('/'):
            url = url[:-1]
        return url

    def poll(self, tree=None):
        data = self._poll(tree=tree)
        if 'jobs' in data:
            data['jobs'] = self.resolve_job_folders(data['jobs'])
        if not tree:
            self._data = data
        else:
            return data

    def _poll(self, tree=None):
        url = self.python_api_url(self.baseurl)
        return self.get_data(url, tree=tree)

    def get_data(self, url, params=None, tree=None):
        requester = self.get_jenkins_obj().requester
        if tree:
            if not params:
                params = {'tree': tree}
            else:
                params.update({'tree': tree})

        response = requester.get_url(url, params)
        if response.status_code != 200:
            logging.error('Failed request at %s with params: %s %s',
                          url, params, tree if tree else '')
            response.raise_for_status()
        try:
            return ast.literal_eval(response.text)
        except Exception:
            logging.exception('Inappropriate content found at %s', url)
            raise JenkinsAPIException('Cannot parse %s' % response.content)

    def pprint(self):
        """Print out all the data in this object for debugging.
        """
        pprint.pprint(self._data)

    def resolve_job_folders(self, jobs):
        for job in list(jobs):
            if 'color' not in job.keys():
                jobs.remove(job)
                jobs += self.process_job_folder(job)

        return jobs

    def process_job_folder(self, folder):
        data = self.get_data(self.python_api_url(folder['url']))
        result = []

        for job in data.get('jobs', []):
            if 'color' not in job.keys():
                result += self.process_job_folder(job)
            else:
                result.append(job)

        return result

    @classmethod
    def python_api_url(cls, url):
        if url.endswith(config.JENKINS_API):
            return url
        else:
            if url.endswith(r"/"):
                fmt = "%s%s"
            else:
                fmt = "%s/%s"
            return fmt % (url, config.JENKINS_API)
