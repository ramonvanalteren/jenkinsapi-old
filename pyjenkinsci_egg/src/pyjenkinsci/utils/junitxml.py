import logging
import datetime
import traceback
import sys

try:
    from xml.etree import ElementTree as ET
except Exception, e:
    import elementtree.ElementTree as ET

from pyjenkinsci.utils.dates import timedelta_to_seconds

log = logging.getLogger(__name__)

class junitxml( object ):

    ERROR = "error"
    FAILURE = "failure"

    def __init__( self, stream, testsuite_name="test", ):
        """
        Set up a new stream
        """
        assert isinstance( testsuite_name, str )

        self.xml = ET.Element("testsuite")
        self.stream = stream

        self.xml.attrib["name"] = testsuite_name

        self.count_errors = 0
        self.count_tests = 0
        self.count_failures = 0

    def __repr__(self):
        return "<%s.%s %s>" % (self.__class__.__module__, self.__class__.__name__, str(self))

    def __str__(self):
        return "Stream: %s, Tests: %i Errors: %i, Failures %i" % ( repr( self.stream ),
                                                                   self.count_tests,
                                                                   self.count_errors,
                                                                   self.count_failures )

    @classmethod
    def get_error_strings( cls, e ):
        str_error_type = "%s.%s" % ( e.__class__.__module__, e.__class__.__name__ )
        str_error_args = ",".join( [repr(ee) for ee in e.args] )
        str_doc = str( e.__doc__ ).strip()

        return str_error_type, str_error_args, str_doc

    def write(self, xml_declaration=True, encoding="utf-8"):
        self.xml.attrib["errors"] = str( self.count_errors )
        self.xml.attrib["failures"] = str( self.count_failures )
        self.xml.attrib["tests"] = str( self.count_tests )

        ET.ElementTree( self.xml ).write( self.stream, encoding=encoding, xml_declaration=xml_declaration )
        log.warn( "Wrote Junit-style XML log to %s" % self.stream )

    def assertTrue(self, classname, testname, errmsg, fn, *args, **kwargs ):
        """
        Map the interface onto an assert like statement.
        Also returns the value so that we can do useful things with the result
        """

        _testname = testname.replace( ".", "_") # Dots are not permitted in names'

        def assert_fn( ):
            if callable(fn):
                assert fn( *args, **kwargs ), errmsg
            else:
                assert len(args) == 0 and len(kwargs) == 0, "Object being tested is not callable and cannot have arguments."
                assert fn, "errmsg"

        tr = self.startTest(classname, _testname)
        return tr.run( assert_fn )

    def startTest( self, classname, testname, ):
        return junitxml_transaction( self, classname, testname )

    def passTest( self, classname, name, test_time ):
        self.addPass( classname, name, test_time)

    def failTest(self, classname, name, test_time, error, tb, mode=FAILURE ):
        """
        Add a error
        """
        str_error, str_error_msg, str_doc = self.get_error_strings( error )
        enhanced_tb = "%s: %s\n\n( %s )\n\n%s" % ( repr(error), str_error_msg, str_doc, tb )
        tc = self.addPass( classname, name, test_time)
        self.convertPassToFail( tc, str_error, enhanced_tb, mode=mode )


    def addPass(self, classname, name, test_time=0.0, ):
        """
        Add a pass
        """
        assert isinstance( classname, str )
        assert isinstance( name, str )
        assert isinstance( test_time, (int, float) )
        self.count_tests += 1
        testcase = ET.SubElement( self.xml, "testcase" )
        testcase.attrib["classname"] = classname
        testcase.attrib["name"] = name
        testcase.attrib["time"] = "%.2f" % test_time

        return testcase

    def convertPassToFail( self, tc, failtype="", tb="", mode=FAILURE ):
        """
        Add a failure
        """
        assert isinstance( failtype, str )
        assert isinstance( tb, str ), "Traceback should be a string, got %s" % repr(tb)
        assert mode in [ self.FAILURE, self.ERROR ]

        if mode == self.FAILURE:
            self.count_errors += 1
        else:
            self.count_failures += 1

        failure = ET.SubElement( tc, mode )
        failure.text = tb
        failure.attrib["type"] = failtype
        return failure


class junitxml_transaction( object ):
    def __init__(self, jxml, classname, testname ):
        assert isinstance( jxml, junitxml )
        self.jxml = jxml
        self.classname = classname
        self.testname = testname
        self.start_time = datetime.datetime.now()

    def getRuntime(self):
        return timedelta_to_seconds( datetime.datetime.now() - self.start_time )

    def run( self, fn, *args, **kwargs ):
        try:
            result = fn( *args, **kwargs )
            self.jxml.addPass( self.classname, self.testname, self.getRuntime() )
        except Exception, e:
            ex_type, ex_value, ex_tb = sys.exc_info()

            tb_formatted = traceback.format_exception( ex_type, ex_value, ex_tb )
            str_tb = "\n".join( tb_formatted )
            str_ex = "%s.%s" % ( ex_value.__class__.__module__, ex_value.__class__.__name__ )
            runtime = self.getRuntime()

            if isinstance(e, AssertionError):
                self.jxml.failTest( self.classname, self.testname, runtime, e, str_tb, mode=self.jxml.FAILURE )
            else:
                self.jxml.failTest( self.classname, self.testname, runtime, e, str_tb, mode=self.jxml.ERROR )

            log.exception(e)

            raise e
        return result

if __name__ == "__main__":
    import sys
    import time
    import random

    logging.basicConfig()
    logging.getLogger("").setLevel( logging.INFO )
    fod = junitxml( stream=sys.stdout )

    def fn_test( mode ):

        time.sleep( random.random( ) )

        if mode=="pass":
            return 1
        elif mode=="fail":
            assert False
        elif mode=="error":
            {}["x"]

    for testname in [ "pass", "fail", "error" ]:
        t = fod.startTest("a", testname, )
        try:
            t.run( fn_test, testname )
        except Exception, e:
            #log.exception(e)
            pass

    fod.write()
