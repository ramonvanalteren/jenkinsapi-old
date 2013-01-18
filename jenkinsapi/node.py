from jenkinsapi.jenkinsbase import JenkinsBase
import logging
import urllib

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
        self.poll()
        return not self._data['offline']

    def is_temporarily_offline(self):
        self.poll()
        return self._data['temporarilyOffline']

    def is_jnlpagent(self):
        return self._data['jnlpAgent']

    def is_idle(self):
        return self._data['idle']


    def set_online(self):
        self.poll()
        if self._data['offline'] and not self._data['temporarilyOffline']:
            raise AssertionError("Node is offline and not marked as temporarilyOffline" + 
                                 ", check client connection: " + 
                                 "offline = %s , temporarilyOffline = %s" % 
                                (self._data['offline'], self._data['temporarilyOffline']))
        elif self._data['offline'] and self._data['temporarilyOffline']:
            self.toggle_temporarily_offline()
            self.poll()
            if self._data['offline']:
                raise AssertionError("The node state is still offline, check client connection:" + 
                                     " offline = %s , temporarilyOffline = %s" % 
                                     (self._data['offline'], self._data['temporarilyOffline']))

    def set_offline(self, message="requested from jenkinsapi"):
        self.poll()
        if not self._data['offline']:
            self.toggle_temporarily_offline(message)
            self.poll()
            if not self._data['offline']:
                raise AssertionError("The node state is still online:" + 
                                     "offline = %s , temporarilyOffline = %s" % 
                                     (self._data['offline'], self._data['temporarilyOffline']))

    def toggle_temporarily_offline(self, message="requested from jenkinsapi"):
        initial_state = self.is_temporarily_offline()
        url = self.baseurl + "/toggleOffline?offlineMessage=" + urllib.quote(message)
        html_result = self.hit_url(url)
        log.debug(html_result)
        if initial_state == self.is_temporarily_offline():
            raise AssertionError("The node state has not changed: temporarilyOffline = %s" % state)
