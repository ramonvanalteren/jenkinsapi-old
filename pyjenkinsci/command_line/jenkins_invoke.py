import os
import sys
import logging
import optparse
from pyjenkinsci import jenkins

log = logging.getLogger(__name__)

class jenkins_invoke(object):
    @classmethod
    def mkparser(cls):
        parser = optparse.OptionParser()
        DEFAULT_BASEURL=os.environ.get( "JENKINS_URL", "http://localhost/jenkins" )
        parser.help_text = "Execute a number of jenkins jobs on the server of your choice. Optionally block until the jobs are complete."
        parser.add_option("-J", "--jenkinsbase", dest="baseurl",
                          help="Base URL for the Jenkins server, default is %s" % DEFAULT_BASEURL,
                          type="str",
                          default=DEFAULT_BASEURL, )
        parser.add_option("-b", "--block", dest="block",
                          help="Block until each of the jobs is complete." ,
                          action="store_true",
                          default=False )
        parser.add_option("-t", "--token", dest="token",
                          help="Optional security token." ,
                          default=None )
        return parser

    @classmethod
    def main(cls):
        parser = cls.mkparser()
        options, args = parser.parse_args()
        try:
            assert len(args) > 0, "Need to specify at least one job name"
        except AssertionError, e:
            log.critical(e[0])
            parser.print_help()
            sys.exit(1)
        invoker = cls(options, args)
        invoker()

    def __init__(self, options, jobs):
        self.options = options
        self.jobs = jobs

    def __call__(self):
        for job in self.jobs:
            self.invokejob(job, block=self.options.block, baseurl=self.options.baseurl, token=self.options.token)

    def invokejob(self, jobname, block, baseurl, token ):
        assert type(block) == bool
        assert type(baseurl) == str
        assert type(jobname) == str
        assert token is None or isinstance(token, str)
        jenkinsserver = jenkins.Jenkins( baseurl )
        job = jenkinsserver[jobname]
        job.invoke(securitytoken=token, block=block)


def main(  ):
    logging.basicConfig()
    logging.getLogger("").setLevel(logging.INFO)
    jenkins_invoke.main()