from optparse import OptionParser

class base( object ):

    @classmethod
    def mkparser(cls):
        parser = OptionParser()
        return parser
