from pyjenkinsci.jenkinsbase import JenkinsBase
from pyjenkinsci.result import Result

class ResultSet(JenkinsBase):
    """
    Represents a result from a completed Jenkins run.
    """
    def get_jenkins_obj(self):
        return self.build.job.get_jenkins_obj()

    def __init__(self, url, build ):
        """
        """
        self.build = build
        JenkinsBase.__init__( self, url )

    def __str__(self):
        return "Test Result for %s" % str( self.build )

    def keys(self):
        return [ a[0] for a in self.iteritems() ]

    def items(self):
        return [a for a in self.iteritems()]

    def iteritems(self):
        for suite in self._data.get("suites", [] ):
            for case in suite["cases"]:
                R = Result( **case )
                yield R.id(), R

        for report_set in self._data.get( "childReports", [] ):
            for suite in report_set["result"]["suites"]:
                for case in suite["cases"]:
                    R = Result( **case )
                    yield R.id(), R

    def __len__(self):
        return sum( 1 for x in self.iteritems()  )
