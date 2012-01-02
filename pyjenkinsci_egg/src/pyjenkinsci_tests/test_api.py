"""
Important: For this test to work we need at least one Jenkins server
You need to configure the JENKINS_BASE environment variable
And you need to enure that this Jenkins has at least one job called "test1".
Make sure that sucsessful builds of test one archive an artifact called "test1.txt" - it can be anything.
"""
import unittest
import logging

from pyjenkinsci.build import build
from pyjenkinsci.result_set import result_set
from pyjenkinsci.result import result
from pyjenkinsci import api
from pyjenkinsci_tests.config import JENKINS_BASE, BUILD_NAME_TEST1

if __name__ == "__main__":
    logging.basicConfig()

log = logging.getLogger(__name__)

class test_api( unittest.TestCase ):
    """
    Perform a number of basic queries.
    """

    def setUp(self):
        pass

    def test_get_latest_build_results(self):
        lb = api.get_latest_build(JENKINS_BASE, BUILD_NAME_TEST1)
        assert isinstance(lb, build)
        rs = lb.get_resultset()
        assert isinstance( rs, result_set )
        assert len(rs) > 0

        for id, res in rs.items():
            assert isinstance( res, result ), "Expected result-set object, got %s" % repr(res)


if __name__ == "__main__":
    unittest.main()
