"""
Module for jenkinsapi nodes
"""

import json
import logging
import urllib
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
        return len(self.iteritems())

    def create_node(self, name, num_executors=2, node_description=None,
                    remote_fs='/var/lib/jenkins', labels=None,
                    exclusive=False, host=None, port=None,
                    credential_descr=None, jvm_options='',
                    java_path=None, prefix_start_slave_cmd='',
                    suffix_start_slave_cmd=''):
        """
        Create a new slave node via SSH.

        :param name: fqdn of slave, str
        :param num_executors: number of executors, int
        :param node_description: a freetext field describing the node
        :param remote_fs: jenkins path, str
        :param labels: labels to associate with slave, str
        :param exclusive: tied to specific job, boolean
        :param host: slave server's host name
        :param port: slave server's port
        :param credential_descr: jenkins credential description field
        :param jvm_options: specify JVM options needed when launching java
        :param java_path: java path
        :param prefix_start_slave_cmd: prefix start slave command
        :param suffix_start_slave_cmd: suffix start slave command
        :return: node obj
        """
        NODE_TYPE = 'hudson.slaves.DumbSlave$DescriptorImpl'
        MODE = 'NORMAL'
        if name in self:
            return self[name]

        if exclusive:
            MODE = 'EXCLUSIVE'
        if not credential_descr:
            launcher = {'stapler-class': 'hudson.slaves.JNLPLauncher'}
        else:
            credential = self.jenkins.credentials.get(credential_descr, None)
            if not credential:
                raise JenkinsAPIException('Credential with description "%s" '
                                          'not found' % credential_descr)
            launcher = {
                'stapler-class': 'hudson.plugins.sshslaves.SSHLauncher',
                'host': host,
                'port': port,
                'credentialsId': credential.credential_id,
                'jvmOptions': jvm_options,
                'javaPath': java_path,
                'prefixStartSlaveCmd': prefix_start_slave_cmd,
                'suffixStartSlaveCmd': suffix_start_slave_cmd
            }

        params = {
            'name': name,
            'type': NODE_TYPE,
            'json': json.dumps({
                'name': name,
                'nodeDescription': node_description,
                'numExecutors': num_executors,
                'remoteFS': remote_fs,
                'labelString': labels,
                'mode': MODE,
                'type': NODE_TYPE,
                'retentionStrategy': {'stapler-class':
                                      'hudson.slaves.'
                                      'RetentionStrategy$Always'},
                'nodeProperties': {'stapler-class-bag': 'true'},
                'launcher': launcher
            })
        }
        url = self.jenkins.get_node_url() + "doCreateItem?%s" % \
            urllib.urlencode(params)
        self.jenkins.requester.get_and_confirm_status(url)
        self.poll()
        return self[name]

    def __delitem__(self, item):
        if item in self and item != 'master':
            url = "%s/doDelete" % self[item].baseurl
            self.jenkins.requester.get_and_confirm_status(url)
            self.poll()
