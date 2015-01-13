import mock
import types
# To run unittests on python 2.6 please use unittest2 library
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from jenkinsapi.custom_exceptions import JenkinsAPIException
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.executors import Executors
from jenkinsapi.executor import Executor


class TestExecutors(unittest.TestCase):

    DATAM = {
        'assignedLabels': [{}],
        'description': None,
        'jobs': [],
        'mode': 'NORMAL',
        'nodeDescription': 'the master Jenkins node',
        'nodeName': '',
        'numExecutors': 2,
        'overallLoad': {},
        'primaryView': {'name': 'All', 'url': 'http://localhost:8080/'},
        'quietingDown': False,
        'slaveAgentPort': 0,
        'unlabeledLoad': {},
        'useCrumbs': False,
        'useSecurity': False,
        'views': [
            {'name': 'All', 'url': 'http://localhost:8080/'},
            {'name': 'BigMoney', 'url': 'http://localhost:8080/view/BigMoney/'}
        ]
    }

    DATA0 = {
        "actions": [
        ],
        "displayName": "host0.host.com",
        "executors": [
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {}
        ],
        "icon": "computer.png",
        "idle": False,
        "jnlpAgent": True,
        "launchSupported": False,
        "loadStatistics": {

        },
        "manualLaunchAllowed": True,
        "monitorData": {
            "hudson.node_monitors.SwapSpaceMonitor": {
                "availablePhysicalMemory": 8462417920,
                "availableSwapSpace": 0,
                "totalPhysicalMemory": 75858042880,
                "totalSwapSpace": 0
            },
            "hudson.node_monitors.ArchitectureMonitor": "Linux (amd64)",
            "hudson.node_monitors.ResponseTimeMonitor": {
                "average": 2
            },
            "hudson.node_monitors.TemporarySpaceMonitor": {
                "path": "/tmp",
                "size": 430744551424
            },
            "hudson.node_monitors.DiskSpaceMonitor": {
                "path": "/data/jenkins",
                "size": 1214028627968
            },
            "hudson.node_monitors.ClockMonitor": {
                "diff": 1
            }
        },
        "numExecutors": 8,
        "offline": False,
        "offlineCause": None,
        "offlineCauseReason": "",
        "oneOffExecutors": [
            {},
            {}
        ],
        "temporarilyOffline": False
    }

    DATA1 = {
        "actions": [
        ],
        "displayName": "host1.host.com",
        "executors": [
            {},
            {}
        ],
        "icon": "computer.png",
        "idle": False,
        "jnlpAgent": True,
        "launchSupported": False,
        "loadStatistics": {
        },
        "manualLaunchAllowed": True,
        "monitorData": {
            "hudson.node_monitors.SwapSpaceMonitor": {
                "availablePhysicalMemory": 8462417920,
                "availableSwapSpace": 0,
                "totalPhysicalMemory": 75858042880,
                "totalSwapSpace": 0
            },
            "hudson.node_monitors.ArchitectureMonitor": "Linux (amd64)",
            "hudson.node_monitors.ResponseTimeMonitor": {
                "average": 2
            },
            "hudson.node_monitors.TemporarySpaceMonitor": {
                "path": "/tmp",
                "size": 430744551424
            },
            "hudson.node_monitors.DiskSpaceMonitor": {
                "path": "/data/jenkins",
                "size": 1214028627968
            },
            "hudson.node_monitors.ClockMonitor": {
                "diff": 1
            }
        },
        "numExecutors": 2,
        "offline": False,
        "offlineCause": None,
        "offlineCauseReason": "",
        "oneOffExecutors": [
            {},
            {}
        ],
        "temporarilyOffline": False
    }

    DATA2 = {
        "actions": [
        ],
        "displayName": "host2.host.com",
        "executors": [
            {},
            {},
            {},
            {}
        ],
        "icon": "computer.png",
        "idle": False,
        "jnlpAgent": True,
        "launchSupported": False,
        "loadStatistics": {
        },
        "manualLaunchAllowed": True,
        "monitorData": {
            "hudson.node_monitors.SwapSpaceMonitor": {
                "availablePhysicalMemory": 8462417920,
                "availableSwapSpace": 0,
                "totalPhysicalMemory": 75858042880,
                "totalSwapSpace": 0
            },
            "hudson.node_monitors.ArchitectureMonitor": "Linux (amd64)",
            "hudson.node_monitors.ResponseTimeMonitor": {
                "average": 2
            },
            "hudson.node_monitors.TemporarySpaceMonitor": {
                "path": "/tmp",
                "size": 430744551424
            },
            "hudson.node_monitors.DiskSpaceMonitor": {
                "path": "/data/jenkins",
                "size": 1214028627968
            },
            "hudson.node_monitors.ClockMonitor": {
                "diff": 1
            }
        },
        "numExecutors": 4,
        "offline": False,
        "offlineCause": None,
        "offlineCauseReason": "",
        "oneOffExecutors": [
            {},
            {}
        ],
        "temporarilyOffline": False
    }

    DATA3 = {
        "actions": [
        ],
        "displayName": "host3.host.com",
        "executors": [
            {}
        ],
        "icon": "computer.png",
        "idle": False,
        "jnlpAgent": True,
        "launchSupported": False,
        "loadStatistics": {},
        "manualLaunchAllowed": True,
        "monitorData": {
            "hudson.node_monitors.SwapSpaceMonitor": {
                "availablePhysicalMemory": 8462417920,
                "availableSwapSpace": 0,
                "totalPhysicalMemory": 75858042880,
                "totalSwapSpace": 0
            },
            "hudson.node_monitors.ArchitectureMonitor": "Linux (amd64)",
            "hudson.node_monitors.ResponseTimeMonitor": {
                "average": 2
            },
            "hudson.node_monitors.TemporarySpaceMonitor": {
                "path": "/tmp",
                "size": 430744551424
            },
            "hudson.node_monitors.DiskSpaceMonitor": {
                "path": "/data/jenkins",
                "size": 1214028627968
            },
            "hudson.node_monitors.ClockMonitor": {
                "diff": 1
            }
        },
        "numExecutors": 1,
        "offline": False,
        "offlineCause": None,
        "offlineCauseReason": "",
        "oneOffExecutors": [
            {},
            {}
        ],
        "temporarilyOffline": False
    }

    EXEC0 = {
        "currentExecutable": {
            "number": 4168,
            "url": "http://localhost:8080/job/testjob/4168/"
        },
        "currentWorkUnit": {},
        "idle": False,
        "likelyStuck": False,
        "number": 0,
        "progress": 48
    }

    EXEC1 = {
        "currentExecutable": None,
        "currentWorkUnit": None,
        "idle": True,
        "likelyStuck": False,
        "number": 0,
        "progress": -1
    }

    @mock.patch.object(Jenkins, '_poll')
    def setUp(self, _poll_jenkins):
        _poll_jenkins.return_value = self.DATAM
        self.J = Jenkins('http://localhost:8080')

    def testRepr(self):
        # Can we produce a repr string for this object
        assert repr(self.J)

    def testCheckURL(self):
        self.assertEquals(self.J.baseurl, 'http://localhost:8080')

    @mock.patch.object(Executors, '_poll')
    @mock.patch.object(Executor, '_poll')
    def testGetExecutors(self, _poll_executor, _poll_executors):
        _poll_executor.return_value = self.EXEC0
        _poll_executors.return_value = self.DATA3
        exec_info = self.J.get_executors(self.DATA3['displayName'])

        self.assertIsInstance(exec_info, object)
        self.assertIsInstance(repr(exec_info), str)

        for e in exec_info:
            self.assertEquals(e.get_progress(), 48, 'Should return 48 %')

    @mock.patch.object(Executors, '_poll')
    @mock.patch.object(Executor, '_poll')
    def testis_idle(self, _poll_executor, _poll_executors):
        _poll_executor.return_value = self.EXEC1
        _poll_executors.return_value = self.DATA3
        exec_info = self.J.get_executors('host3.host.com')

        self.assertIsInstance(exec_info, object)
        for e in exec_info:
            self.assertEquals(e.get_progress(), -1, 'Should return 48 %')
            self.assertEquals(e.is_idle(), True, 'Should return True')
            self.assertEquals(
                repr(e),
                '<jenkinsapi.executor.Executor host3.host.com 0>'
            )

    @mock.patch.object(Executor, '_poll')
    def test_likely_stuck(self, _poll_executor):
        _poll_executor.return_value = self.EXEC0
        baseurl = 'http://localhost:8080/computer/host0.host.com/executors/0'
        nodename = 'host0.host.com'
        single_executer = Executor(baseurl, nodename, self.J, '0')
        self.assertEquals(single_executer.likely_stuck(), False)

    @mock.patch.object(Executor, '_poll')
    def test_get_current_executable(self, _poll_executor):
        _poll_executor.return_value = self.EXEC0
        baseurl = 'http://localhost:8080/computer/host0.host.com/executors/0'
        nodename = 'host0.host.com'
        single_executer = Executor(baseurl, nodename, self.J, '0')
        self.assertEquals(
            single_executer.get_current_executable()['number'],
            4168
        )
        self.assertEquals(
            single_executer.get_current_executable()['url'],
            'http://localhost:8080/job/testjob/4168/'
        )


if __name__ == '__main__':
    unittest.main()
