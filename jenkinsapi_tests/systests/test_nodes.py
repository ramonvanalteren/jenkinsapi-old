'''
System tests for `jenkinsapi.jenkins` module.
'''
import logging
import pytest
from jenkinsapi.node import Node
from jenkinsapi.credential import SSHKeyCredential
from jenkinsapi_tests.test_utils.random_strings import random_string

log = logging.getLogger(__name__)


def test_online_offline(jenkins):
    """
    Can we flip the online / offline state of the master node.
    """
    # Master node name should be case insensitive
    # mn0 = jenkins.get_node('MaStEr')
    mn = jenkins.get_node('master')
    # self.assertEquals(mn, mn0)

    mn.set_online()  # It should already be online, hence no-op
    assert mn.is_online() is True

    mn.set_offline()  # We switch that suckah off
    mn.set_offline()  # This should be a no-op
    assert mn.is_online() is False

    mn.set_online()  # Switch it back on
    assert mn.is_online() is True


def test_create_jnlp_node(jenkins):
    node_name = random_string()
    node_dict = {
        'num_executors': 1,
        'node_description': 'Test JNLP Node',
        'remote_fs': '/tmp',
        'labels': 'systest_jnlp',
        'exclusive': True
    }
    node = jenkins.nodes.create_node(node_name, node_dict)
    assert isinstance(node, Node) is True

    del jenkins.nodes[node_name]


def test_create_ssh_node(jenkins):
    node_name = random_string()
    creds = jenkins.get_credentials()

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
    node = jenkins.nodes.create_node(node_name, node_dict)
    assert isinstance(node, Node) is True
    del jenkins.nodes[node_name]

    jenkins.nodes[node_name] = node_dict
    assert isinstance(jenkins.nodes[node_name], Node) is True
    del jenkins.nodes[node_name]


def test_delete_node(jenkins):
    node_name = random_string()
    node_dict = {
        'num_executors': 1,
        'node_description': 'Test JNLP Node',
        'remote_fs': '/tmp',
        'labels': 'systest_jnlp',
        'exclusive': True
    }
    jenkins.nodes.create_node(node_name, node_dict)
    del jenkins.nodes[node_name]

    with pytest.raises(KeyError):
        jenkins.nodes[node_name]

    with pytest.raises(KeyError):
        del jenkins.nodes['not_exist']


def test_delete_all_nodes(jenkins):
    nodes = jenkins.nodes

    for name in nodes.keys():
        del nodes[name]

    assert len(jenkins.nodes) == 1


def test_get_node_labels(jenkins):
    node_name = random_string()
    node_labels = 'LABEL1 LABEL2'
    node_dict = {
        'num_executors': 1,
        'node_description': 'Test Node with Labels',
        'remote_fs': '/tmp',
        'labels': node_labels,
        'exclusive': True
    }
    node = jenkins.nodes.create_node(node_name, node_dict)
    assert node.get_labels() == node_labels
    del jenkins.nodes[node_name]
