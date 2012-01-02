from pyjenkinsci.jenkinsbase import JenkinsBase
from pyjenkinsci.job import Job

class View(JenkinsBase):

    def __init__(self, url, name, jenkins_obj):
        self.name = name
        self.jenkins_obj = jenkins_obj
        JenkinsBase.__init__(self, url)

    def __str__(self):
        return self.name

    def __getitem__(self, str_job_id ):
        assert isinstance( str_job_id, str )
        api_url = self.python_api_url( self.get_job_url( str_job_id ) )
        return Job( api_url, str_job_id, self.jenkins_obj )

    def keys(self):
        return self.get_job_dict().keys()

    def iteritems(self):
        for name, url in self.get_job_dict().iteritems():
            api_url = self.python_api_url( url )
            yield name, Job( api_url, name, self.jenkins_obj )

    def values(self):
        return [ a[1] for a in self.iteritems() ]

    def items(self):
        return [ a for a in self.iteritems() ]

    def _get_jobs( self ):
        if not self._data.has_key( "jobs" ):
            pass
        else:
            for viewdict in self._data["jobs"]:
                yield viewdict["name"], viewdict["url"]

    def get_job_dict(self):
        return dict( self._get_jobs() )

    def __len__(self):
        return len( self.get_job_dict().keys() )

    def get_job_url( self, str_job_name ):
        try:
            job_dict = self.get_job_dict()
            return job_dict[ str_job_name ]
        except KeyError, ke:
            all_views = ", ".join( job_dict.keys() )
            raise KeyError("Job %s is not known - available: %s" % ( str_job_name, all_views ) )

    def get_jenkins_obj(self):
        return self.jenkins_obj

    def id(self):
        """
        Calculate an ID for this object.
        """
        return "%s.%s" % ( self.className, self.name )