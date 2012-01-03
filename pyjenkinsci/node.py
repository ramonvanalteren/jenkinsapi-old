from pyjenkinsci.jenkinsbase import JenkinsBase
import logging

log = logging.getLogger(__name__)

class Node(JenkinsBase):
    """
    Class to hold information on nodes that are attached as slaves to the master jenkins instance
    """

    def __init__(self, baseurl, nodename, jenkins_obj):
        """
        Init a node object by providing all relevant pointers to it
        :param baseurl: basic url for querying information on a node
        :param nodename: hostname of the node
        :param jenkins_obj: ref to the jenkins obj
        :return: Node obj
        """
        self.name = nodename
        self.jenkins = jenkins_obj
        JenkinsBase.__init__(self, baseurl)

    def get_jenkins_obj(self):
        return self.jenkins

    def id(self):
        return self.name

    def __str__(self):
        return self.id()

    def get_node_data(self):
        return self._data

    def is_online(self):
        return not self._data['offline']

    def is_jnlpagent(self):
        return self._data['jnlpAgent']

    def is_idle(self):
        return self._data['idle']

