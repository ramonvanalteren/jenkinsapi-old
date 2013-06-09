import logging
from jenkinsapi.node import Node
from jenkinsapi.jenkinsbase import JenkinsBase

log = logging.getLogger(__name__)

class Nodes(JenkinsBase):
    """
    Class to hold information on a collection of nodes
    """

    def __init__(self, baseurl, jenkins_obj):
        """
        Handy access to all of the nodes on your Jenkins server
        """
        self.jenkins = jenkins_obj
        JenkinsBase.__init__(self, baseurl)

    def __str__(self):
        return 'Nodes @ %s' % self.baseurl

    def iteritems(self):
        for item in self._data['computer']:
            nodename = item['displayName']
            if nodename == 'master':
                nodeurl = '%s/(%s)' % (self.baseurl, nodename)
            else:
                nodeurl = '%s/%s' % (self.baseurl, nodename)
            yield item['displayName'], Node(nodeurl, nodename, self.jenkins)

    def __getitem__(self, nodename):
        for k, v in self.iteritems():
            if k == nodename:
                return v
