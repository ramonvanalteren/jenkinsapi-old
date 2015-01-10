'''
System tests for `jenkinsapi.jenkins` module.
'''
import logging
# To run unittests on python 2.6 please use unittest2 library
try:
    import unittest2 as unittest
except ImportError:
    import unittest
from jenkinsapi.node import Node
from jenkinsapi.credential import UsernamePasswordCredential
from jenkinsapi_tests.systests.base import BaseSystemTest
from jenkinsapi_tests.test_utils.random_strings import random_string

log = logging.getLogger(__name__)


class TestNodes(BaseSystemTest):

    def test_online_offline(self):
        """
        Can we flip the online / offline state of the master node.
        """
        # Master node name should be case insensitive
        # mn0 = self.jenkins.get_node('MaStEr')
        mn = self.jenkins.get_node('master')
        # self.assertEquals(mn, mn0)

        mn.set_online()  # It should already be online, hence no-op
        self.assertTrue(mn.is_online())

        mn.set_offline()  # We switch that suckah off
        mn.set_offline()  # This should be a no-op
        self.assertFalse(mn.is_online())

        mn.set_online()  # Switch it back on
        self.assertTrue(mn.is_online())

    def test_create_jnlp_node(self):
        node_name = random_string()
        node = self.jenkins.create_node(node_name, 2, 'test')

        self.assertTrue(isinstance(node, Node))

        node2 = self.jenkins.create_node(node_name, 2, 'test')
        self.assertEquals(node, node2)

    def test_create_ssh_node(self):
        node_name = random_string()
        creds = self.jenkins.get_credentials()

        cred_descr = random_string()
        creds[cred_descr] = UsernamePasswordCredential('username', 'password')
        node_dict = {
            'num_executors': 1,
            'node_description': 'Description %s' % node_name,
            'remote_fs': '/tmp',
            'labels': node_name,
            'exclusive': False,
            'host': 'localhost',
            'port': 22,
            'credential_description': cred_descr,
            'jvm_options': '',
            'java_path': '',
            'prefix_start_slave_cmd': '',
            'suffix_start_slave_cmd': ''
        }
        self.jenkins.nodes[node_name] = Node(baseurl=None,
                                             nodename=node_name,
                                             jenkins_obj=self.jenkins,
                                             node_dict=node_dict)

        node = self.jenkins.nodes[node_name]

        self.assertTrue(isinstance(node, Node))

    def test_delete_node(self):
        node_name = random_string()
        self.jenkins.create_node(node_name, 2, 'test')
        del self.jenkins.nodes[node_name]

        with self.assertRaises(KeyError):
            self.jenkins.nodes[node_name]

    def test_delete_all_nodes(self):
        nodes = self.jenkins.nodes

        for name in nodes.keys():
            del nodes[name]

        self.assertTrue(len(self.jenkins.nodes) == 1)


if __name__ == '__main__':
    logging.basicConfig()
    unittest.main()
