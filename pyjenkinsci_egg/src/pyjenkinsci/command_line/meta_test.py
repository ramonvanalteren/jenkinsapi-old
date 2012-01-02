import optparse
import os
import random
import logging
from pyjenkinsci.utils import junitxml
from pyjenkinsci.utils.id import mk_id

log = logging.getLogger(__name__)

class meta_test(object):
    ATTEMPTS=3

    @classmethod
    def mkParser(cls):
        parser = optparse.OptionParser()

    def __init__(self, opts=None):
        self.opts = opts

    def testFunction(self):
        if random.random() < 0.1:
            raise AssertionError("The value was too small")
        return 0

    def __call__(self):
        temp_dir = os.environ.get("TEMP", r"c:\temp" )
        output_dir = os.environ.get( "WORKSPACE", temp_dir )
        result_filepath = os.path.join( output_dir, "results.xml" )
        stream = open( result_filepath, "wb" )
        testsuite_name = mk_id()
        ju = junitxml.junitxml(  stream, testsuite_name)


        classname = mk_id()
        for i in xrange(0, self.ATTEMPTS ):
            tr = ju.startTest( classname, mk_id() )
            try:
                tr.run( self.testFunction )
            except Exception, e:
                log.exception(e)
                continue

        ju.write()

def main( ):
    logging.basicConfig()
    return meta_test()()

if __name__ == "__main__":
    main()
