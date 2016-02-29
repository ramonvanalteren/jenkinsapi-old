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
from jenkinsapi.credential import SSHKeyCredential
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
        node_dict = {
            'num_executors': 1,
            'node_description': 'Test JNLP Node',
            'remote_fs': '/tmp',
            'labels': 'systest_jnlp',
            'exclusive': True
        }
        node = self.jenkins.nodes.create_node(node_name, node_dict)
        self.assertTrue(isinstance(node, Node))

        del self.jenkins.nodes[node_name]

    def test_create_ssh_node(self):
        node_name = random_string()
        creds = self.jenkins.get_credentials()

        cred_descr = random_string()
        cred_dict = {
            'description': cred_descr,
            'userName': 'username',
            'passphrase': '',
            'private_key': '~'
        }
        creds[cred_descr] = SSHKeyCredential(cred_dict)
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
            'suffix_start_slave_cmd': '',
            'retention': 'ondemand',
            'ondemand_delay': 0,
            'ondemand_idle_delay': 5
        }
        node = self.jenkins.nodes.create_node(node_name, node_dict)
        self.assertTrue(isinstance(node, Node))
        del self.jenkins.nodes[node_name]

        self.jenkins.nodes[node_name] = node_dict
        self.assertTrue(isinstance(self.jenkins.nodes[node_name], Node))
        del self.jenkins.nodes[node_name]

    def test_delete_node(self):
        node_name = random_string()
        node_dict = {
            'num_executors': 1,
            'node_description': 'Test JNLP Node',
            'remote_fs': '/tmp',
            'labels': 'systest_jnlp',
            'exclusive': True
        }
        self.jenkins.nodes.create_node(node_name, node_dict)
        del self.jenkins.nodes[node_name]

        with self.assertRaises(KeyError):
            self.jenkins.nodes[node_name]

        with self.assertRaises(KeyError):
            del self.jenkins.nodes['not_exist']

    def test_delete_all_nodes(self):
        nodes = self.jenkins.nodes

        for name in nodes.keys():
            del nodes[name]

        self.assertTrue(len(self.jenkins.nodes) == 1)

    def test_get_node_labels(self):
        node_name = random_string()
        node_labels = 'LABEL1 LABEL2'
        node_dict = {
            'num_executors': 1,
            'node_description': 'Test Node with Labels',
            'remote_fs': '/tmp',
            'labels': node_labels,
            'exclusive': True
        }
        node = self.jenkins.nodes.create_node(node_name, node_dict)
        self.assertEquals(node.get_labels(), node_labels)
        del self.jenkins.nodes[node_name]


if __name__ == '__main__':
    logging.basicConfig()
    unittest.main()
