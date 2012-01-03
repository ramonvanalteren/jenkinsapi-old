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

    def is_online(self):
        return not self._data['offline']

#NODES       = 'computer/api/json'
#CREATE_NODE = 'computer/doCreateItem?%s'
#DELETE_NODE = 'computer/%(name)s/doDelete'
#NODE_INFO   = 'computer/%(name)s/api/json?depth=0'
#NODE_TYPE   = 'hudson.slaves.DumbSlave$DescriptorImpl'
#
#def get_nodes(self):
#    '''
#    Get a list of nodes registered on the jenkins instance
#    returns a list of node dictionaries
#    '''
#    try:
#        response = self.jenkins_open(urllib2.Request(self.server + NODES%locals()))
#        if response:
#            return json.loads(response)['computer']
#        else:
#            raise JenkinsException('Cannot get nodes information')
#    except urllib2.HTTPError:
#        raise JenkinsException('Cannot get nodes information')
#    except ValueError:
#        raise JenkinsException("Could not parse JSON info for nodes information")
#
#def get_node_info(self, name):
#    '''
#    Get node information dictionary
#
#    :param name: Node name, ``str``
#    :returns: Dictionary of node info, ``dict``
#    '''
#    try:
#        response = self.jenkins_open(urllib2.Request(self.server + NODE_INFO%locals()))
#        if response:
#            return json.loads(response)
#        else:
#            raise JenkinsException('node[%s] does not exist'%name)
#    except urllib2.HTTPError:
#        raise JenkinsException('node[%s] does not exist'%name)
#    except ValueError:
#        raise JenkinsException("Could not parse JSON info for node[%s]"%name)
#
#def node_exists(self, name):
#    '''
#    :param name: Name of Jenkins node, ``str``
#    :returns: ``True`` if Jenkins node exists
#    '''
#    try:
#        self.get_node_info(name)
#        return True
#    except JenkinsException:
#        return False
#
#def delete_node(self, name):
#    '''
#    Delete Jenkins node permanently.
#
#    :param name: Name of Jenkins node, ``str``
#    '''
#    self.get_node_info(name)
#    self.jenkins_open(urllib2.Request(self.server + DELETE_NODE%locals(), ''))
#    if self.node_exists(name):
#        raise JenkinsException('delete[%s] failed'%(name))
#
#def create_node(self, name, numExecutors=2, nodeDescription=None,
#                remoteFS='/var/lib/jenkins', labels=None, exclusive=False):
#    '''
#    :param name: name of node to create, ``str``
#    :param numExecutors: number of executors for node, ``int``
#    :param nodeDescription: Description of node, ``str``
#    :param remoteFS: Remote filesystem location to use, ``str``
#    :param labels: Labels to associate with node, ``str``
#    :param exclusive: Use this node for tied jobs only, ``bool``
#    '''
#    if self.node_exists(name):
#        raise JenkinsException('node[%s] already exists'%(name))
#
#    mode = 'NORMAL'
#    if exclusive:
#        mode = 'EXCLUSIVE'
#
#    params = {
#        'name' : name,
#        'type' : NODE_TYPE,
#        'json' : json.dumps ({
#            'name'            : name,
#            'nodeDescription' : nodeDescription,
#            'numExecutors'    : numExecutors,
#            'remoteFS'        : remoteFS,
#            'labelString'     : labels,
#            'mode'            : mode,
#            'type'            : NODE_TYPE,
#            'retentionStrategy' : { 'stapler-class'  : 'hudson.slaves.RetentionStrategy$Always' },
#            'nodeProperties'    : { 'stapler-class-bag' : 'true' },
#            'launcher'          : { 'stapler-class' : 'hudson.slaves.JNLPLauncher' }
#        })
#    }
#
#    self.jenkins_open(urllib2.Request(self.server + CREATE_NODE%urllib.urlencode(params)))
#    if not self.node_exists(name):
#        raise JenkinsException('create[%s] failed'%(name))
