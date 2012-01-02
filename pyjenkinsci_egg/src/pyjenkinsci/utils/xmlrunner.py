"""
XML Test Runner for PyUnit
"""

# Written by Sebastian Rittau <srittau@jroger.in-berlin.de> and placed in
# the Public Domain.

__revision__ = "$Id: /mirror/jroger/python/stdlib/xmlrunner.py 3506 2006-07-27T09:12:39.629878Z srittau  $"

import sys
import time
import traceback
import unittest
import logging
from StringIO import StringIO
from xml.sax.saxutils import escape

log = logging.getLogger()

from pyjenkinsci.utils.bufwrapper import bufwrapper

class faketest( object ):
    """
    A fake test object for when you want to inject additional results into the XML stream.
    """
    failureException = AssertionError

    def __init__( self, id, exc_info ):
        self._id = id
        self._exc_info = exc_info

    def id(self):
        return self._id

    def run(self, result):
        result.startTest(self)
        result.addError(self, self._exc_info )
        ok = False
        result.stopTest(self)

    def __call__(self, *args, **kwds):
        return self.run(*args, **kwds)


class _TestInfo(object):
    """Information about a particular test.
    Used by _XmlTestResult."""

    def __init__( self, test, time, ):
        (self._class, self._method) = test.id().rsplit(".", 1)
        self._time = time
        self._error = None
        self._failure = None
        self._console = ""

    @staticmethod
    def create_success(test, time):
        """Create a _TestInfo instance for a successful test."""
        return _TestInfo(test, time)

    @staticmethod
    def create_failure(test, time, failure, console=""):
        """Create a _TestInfo instance for a failed test."""
        info = _TestInfo(test, time)
        info._failure = failure
        info.console = console
        return info

    @staticmethod
    def create_error(test, time, error, console="" ):
        """Create a _TestInfo instance for an erroneous test."""
        info = _TestInfo(test, time)
        info._error = error
        info.console = console
        return info

    def print_report(self, stream):
        """Print information about this test case in XML format to the
        supplied stream.
        """
        stream.write('  <testcase classname="%(class)s" name="%(method)s" time="%(time).4f">' % \
            {
                "class": self._class,
                "method": self._method,
                "time": self._time,
            })
        if self._failure is not None:
            self._print_error(stream, 'failure', self._failure)
        if self._error is not None:
            self._print_error(stream, 'error', self._error)
        stream.write('</testcase>\n')

    def _print_error(self, stream, tagname, error):
        """Print information from a failure or error to the supplied stream."""
        text = escape(str(error[1]))
        stream.write('\n')
        stream.write('    <%s type="%s">%s\n%s\n' \
            % (tagname, str(error[0]), text, self.console ))
        tb_stream = StringIO()
        traceback.print_tb(error[2], None, tb_stream)
        stream.write(escape(tb_stream.getvalue()))
        stream.write('    </%s>\n' % tagname)
        stream.write('  ')


class _XmlTestResult(unittest.TestResult):
    """A test result class that stores result as XML.

    Used by XmlTestRunner.
    """

    test_count = 0

    @classmethod
    def get_test_serial( cls ):
        cls.test_count += 1
        return cls.test_count

    def __init__(self, classname, consolestream =None ):
        unittest.TestResult.__init__(self)
        self._test_name = classname
        self._start_time = None
        self._tests = []
        self._error = None
        self._failure = None
        self._consolestream = consolestream

    def startTest(self, test):
        unittest.TestResult.startTest(self, test)

        sn = self.get_test_serial()

        log.info( "Test %i: %s" % ( sn, test.id() ) )
        self._error = None
        self._failure = None
        self._start_time = time.time()

    def stopTest(self, test, time_taken = None ):
        if time_taken is not None:
            time_taken = time.time() - self._start_time

        str_console = self._consolestream.get_and_clear()

        unittest.TestResult.stopTest(self, test)
        if self._error:
            info = _TestInfo.create_error(test, time_taken, self._error, console=str_console )
            log.error( "Error: %s" % test.id() )
        elif self._failure:
            info = _TestInfo.create_failure(test, time_taken, self._failure, console=str_console )
            log.error( "Fail: %s" % test.id() )
        else:
            info = _TestInfo.create_success(test, time_taken, )
            log.debug( "OK: %s" % test.id() )
        self._tests.append(info)

    def addError(self, test, err):
        log.warn( "Error: %s" % test.id() )
        unittest.TestResult.addError(self, test, err)
        self._error = err

    def addFailure(self, test, err):
        log.warn( "Failure: %s" % test.id() )
        unittest.TestResult.addFailure(self, test, err)
        self._failure = err

    def print_report(self, stream, time_taken, out, err):
        """Prints the XML report to the supplied stream.

        The time the tests took to perform as well as the captured standard
        output and standard error streams must be passed in.
        """
        stream.write('<testsuite errors="%(e)d" failures="%(f)d" ' % \
            { "e": len(self.errors), "f": len(self.failures) })
        stream.write('name="%(n)s" tests="%(t)d" time="%(time).3f">\n' % \
            {
                "n": self._test_name,
                "t": self.testsRun,
                "time": time_taken,
            })
        for info in self._tests:
            info.print_report(stream)
        stream.write('  <system-out><![CDATA[%s]]></system-out>\n' % out)
        stream.write('  <system-err><![CDATA[%s]]></system-err>\n' % err)
        stream.write('</testsuite>\n')


class XmlTestRunner(object):
    """A test runner that stores results in XML format compatible with JUnit.

    XmlTestRunner(stream=None) -> XML test runner

    The XML file is written to the supplied stream. If stream is None, the
    results are stored in a file called TEST-<module>.<class>.xml in the
    current working directory (if not overridden with the path property),
    where <module> and <class> are the module and class name of the test class.
    """
    def __init__(self, stream=None ):
        self._stream = stream

    @staticmethod
    def get_test_class_name_from_testobj( obj_test ):
        class_ = obj_test.__class__
        classname = class_.__module__ + "." + class_.__name__
        return classname


    def run(self, test, result=None ):
        """Run the given test case or test suite."""
        classname = self.get_test_class_name_from_testobj( test )
        assert not self._stream is None
        stream = self._stream

        # TODO: Python 2.5: Use the with statement
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = bufwrapper( old_stdout )
        sys.stderr = bufwrapper( old_stderr )

        if result is None:
            result = _XmlTestResult( classname, consolestream = sys.stdout )
        else:
            log.debug("Using provided XML test result object.")

        start_time = time.time()

        try:
            test(result)
            try:
                out_s = sys.stdout.getvalue()
            except AttributeError:
                out_s = ""
            try:
                err_s = sys.stderr.getvalue()
            except AttributeError:
                err_s = ""
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        time_taken = time.time() - start_time
        result.print_report(stream, time_taken, out_s, err_s)
        if self._stream is None:
            stream.close()

        return result
