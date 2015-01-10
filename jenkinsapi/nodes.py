"""
Module for jenkinsapi nodes
"""

import logging
try:
    from urllib import urlencode
except ImportError:
    # Python3
    from urllib.parse import urlencode
from jenkinsapi.node import Node
from jenkinsapi.jenkinsbase import JenkinsBase
from jenkinsapi.custom_exceptions import JenkinsAPIException
from jenkinsapi.custom_exceptions import UnknownNode

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

    def get_jenkins_obj(self):
        return self.jenkins

    def __str__(self):
        return 'Nodes @ %s' % self.baseurl

    def __contains__(self, node_name):
        return node_name in self.keys()

    def iterkeys(self):
        for item in self._data['computer']:
            yield item['displayName']

    def keys(self):
        return list(self.iterkeys())

    def iteritems(self):
        for item in self._data['computer']:
            nodename = item['displayName']
            if nodename.lower() == 'master':
                nodeurl = '%s/(%s)' % (self.baseurl, nodename)
            else:
                nodeurl = '%s/%s' % (self.baseurl, nodename)
            try:
                yield item['displayName'], Node(nodeurl,
                                                nodename, self.jenkins)
            except Exception:
                raise JenkinsAPIException('Unable to iterate nodes')

    def __getitem__(self, nodename):
        self_as_dict = dict(self.iteritems())
        if nodename in self_as_dict:
            return self_as_dict[nodename]
        else:
            raise UnknownNode(nodename)

    def __len__(self):
        return len(self.keys())

    def create_jnlp_node(self, name, num_executors=2, node_description=None,
                         remote_fs='/var/lib/jenkins', labels=None,
                         exclusive=False):
        """
        Create a new JNLP slave node

        To create SSH slave use Nodes['new_slave'] = Node()

        :param str name: name of slave
        :param int num_executors: number of executors
        :param str node_description: a freetext field describing the node
        :param str remote_fs: jenkins path
        :param str labels: labels to associate with slave
        :param bool exclusive: tied to specific job
        :return: node obj
        """
        if name in self:
            return self[name]

        # For backwards compatibility we save this old function, but let it
        # use new way of adding node
        node_dict = {
            'num_executors': num_executors,
            'node_description': node_description,
            'remote_fs': remote_fs,
            'labels': labels,
            'exclusive': exclusive
        }

        self[name] = Node(baseurl=None, nodename=name,
                          jenkins_obj=self, poll=False,
                          node_dict=node_dict)

        # url = ('%sdoCreateItem?%s"
        #        % (self.jenkins.get_node_url(), urllib.urlencode(params)))
        # self.jenkins.requester.get_and_confirm_status(url)
        self.poll()
        return self[name]

    def __delitem__(self, item):
        if item in self and item != 'master':
            url = "%s/doDelete" % self[item].baseurl
            self.jenkins.requester.post_and_confirm_status(url, data={})
            self.poll()

    def __setitem__(self, name, node):
        if name not in self:
            url = ('%s/computer/doCreateItem?%s'
                   % (self.jenkins.baseurl,
                      urlencode(node.get_node_attributes())))
            data = {'json': urlencode(node.get_node_attributes())}
            self.jenkins.requester.post_and_confirm_status(url,
                                                           data=data)
            self.poll()
