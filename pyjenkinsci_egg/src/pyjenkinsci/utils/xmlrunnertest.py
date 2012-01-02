import unittest
import sys
import re
from cStringIO import StringIO
from pyjenkinsci.utils.xmlrunner import XmlTestRunner

class XmlTestRunnerTest(unittest.TestCase):
    def setUp(self):
        self._stream = StringIO()

    def _try_test_run(self, test_class, expected):
        """Run the test suite against the supplied test class and compare the
        XML result against the expected XML string. Fail if the expected
        string doesn't match the actual string. All time attribute in the
        expected string should have the value "0.000". All error and failure
        messages are reduced to "Foobar".
        """
        runner = XmlTestRunner(self._stream)
        runner.run(unittest.makeSuite(test_class))

        got = self._stream.getvalue()
        # Replace all time="X.YYY" attributes by time="0.000" to enable a
        # simple string comparison.
        got = re.sub(r'time="\d+\.\d+"', 'time="0.000"', got)
        # Likewise, replace all failure and error messages by a simple "Foobar"
        # string.
        got = re.sub(r'(?s)<failure (.*?)>.*?</failure>', r'<failure \1>Foobar</failure>', got)
        got = re.sub(r'(?s)<error (.*?)>.*?</error>', r'<error \1>Foobar</error>', got)

        self.assertEqual(expected, got)

    def test_no_tests(self):
        """Regression test: Check whether a test run without any tests
        matches a previous run."""
        class TestTest(unittest.TestCase):
            pass
        self._try_test_run(TestTest, """<testsuite errors="0" failures="0" name="unittest.TestSuite" tests="0" time="0.000">
  <system-out><![CDATA[]]></system-out>
  <system-err><![CDATA[]]></system-err>
</testsuite>
""")

    def test_success(self):
        """Regression test: Check whether a test run with a successful test
        matches a previous run."""
        class TestTest(unittest.TestCase):
            def test_foo(self):
                pass
        self._try_test_run(TestTest, """<testsuite errors="0" failures="0" name="unittest.TestSuite" tests="1" time="0.000">
  <testcase classname="__main__.TestTest" name="test_foo" time="0.000"></testcase>
  <system-out><![CDATA[]]></system-out>
  <system-err><![CDATA[]]></system-err>
</testsuite>
""")

    def test_failure(self):
        """Regression test: Check whether a test run with a failing test
        matches a previous run."""
        class TestTest(unittest.TestCase):
            def test_foo(self):
                self.assert_(False)
        self._try_test_run(TestTest, """<testsuite errors="0" failures="1" name="unittest.TestSuite" tests="1" time="0.000">
  <testcase classname="__main__.TestTest" name="test_foo" time="0.000">
    <failure type="exceptions.AssertionError">Foobar</failure>
  </testcase>
  <system-out><![CDATA[]]></system-out>
  <system-err><![CDATA[]]></system-err>
</testsuite>
""")

    def test_error(self):
        """Regression test: Check whether a test run with a erroneous test
        matches a previous run."""
        class TestTest(unittest.TestCase):
            def test_foo(self):
                raise IndexError()
        self._try_test_run(TestTest, """<testsuite errors="1" failures="0" name="unittest.TestSuite" tests="1" time="0.000">
  <testcase classname="__main__.TestTest" name="test_foo" time="0.000">
    <error type="exceptions.IndexError">Foobar</error>
  </testcase>
  <system-out><![CDATA[]]></system-out>
  <system-err><![CDATA[]]></system-err>
</testsuite>
""")

    def test_stdout_capture(self):
        """Regression test: Check whether a test run with output to stdout
        matches a previous run."""
        class TestTest(unittest.TestCase):
            def test_foo(self):
                print "Test"
        self._try_test_run(TestTest, """<testsuite errors="0" failures="0" name="unittest.TestSuite" tests="1" time="0.000">
  <testcase classname="__main__.TestTest" name="test_foo" time="0.000"></testcase>
  <system-out><![CDATA[Test
]]></system-out>
  <system-err><![CDATA[]]></system-err>
</testsuite>
""")

    def test_stderr_capture(self):
        """Regression test: Check whether a test run with output to stderr
        matches a previous run."""
        class TestTest(unittest.TestCase):
            def test_foo(self):
                print >>sys.stderr, "Test"
        self._try_test_run(TestTest, """<testsuite errors="0" failures="0" name="unittest.TestSuite" tests="1" time="0.000">
  <testcase classname="__main__.TestTest" name="test_foo" time="0.000"></testcase>
  <system-out><![CDATA[]]></system-out>
  <system-err><![CDATA[Test
]]></system-err>
</testsuite>
""")

    class NullStream(object):
        """A file-like object that discards everything written to it."""
        def write(self, buffer):
            pass

    def test_unittests_changing_stdout(self):
        """Check whether the XmlTestRunner recovers gracefully from unit tests
        that change stdout, but don't change it back properly.
        """
        class TestTest(unittest.TestCase):
            def test_foo(self):
                sys.stdout = XmlTestRunnerTest.NullStream()

        runner = XmlTestRunner(self._stream)
        runner.run(unittest.makeSuite(TestTest))

    def test_unittests_changing_stderr(self):
        """Check whether the XmlTestRunner recovers gracefully from unit tests
        that change stderr, but don't change it back properly.
        """
        class TestTest(unittest.TestCase):
            def test_foo(self):
                sys.stderr = XmlTestRunnerTest.NullStream()

        runner = XmlTestRunner(self._stream)
        runner.run(unittest.makeSuite(TestTest))


if __name__ == "__main__":
    suite = unittest.makeSuite(XmlTestRunnerTest)
    unittest.TextTestRunner().run(suite)
