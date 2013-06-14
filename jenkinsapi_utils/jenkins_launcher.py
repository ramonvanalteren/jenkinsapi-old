import os
import time
import shutil
import logging
import subprocess
import tempfile
import Queue
import threading

log = logging.getLogger(__name__)

class FailedToStart(Exception): pass

class TimeOut(Exception): pass

class StreamThread(threading.Thread):

    def __init__(self, name, q, stream, fn_log):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q
        self.stream = stream
        self.fn_log = fn_log

    def run(self):
        log.info("Starting %s", self.name)

        while True:
            line = self.stream.readline()
            if line:
                self.fn_log(line.rstrip())
                self.q.put((self.name, line))
            else:
                break
        self.q.put((self.name, None))

class JenkinsLancher(object):
    """
    Launch jenkins
    """
    def __init__(self, war_path):
        self.war_path = war_path
        self.war_directory, self.war_filename = os.path.split(self.war_path)
        self.jenkins_home = tempfile.mkdtemp(prefix='jenkins-home-')
        self.jenkins_process = None
        self.q = Queue.Queue()

    def stop(self):
        log.info("Shutting down jenkins.")
        self.jenkins_process.terminate()
        self.jenkins_process.wait()
        shutil.rmtree(self.jenkins_home)

    def start(self, timeout=30):
        os.environ['JENKINS_HOME'] = self.jenkins_home
        os.chdir(self.war_directory)

        jenkins_command = 'java -jar %s' % self.war_filename

        log.info("About to start Jenkins...")
        log.info("%s> %s", os.getcwd(), jenkins_command)
        self.jenkins_process = subprocess.Popen(
            jenkins_command.split(), stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        threads = [
            StreamThread('out', self.q, self.jenkins_process.stdout, log.info),
            StreamThread('err', self.q, self.jenkins_process.stderr, log.warn)
        ]

        # Start the threads
        for t in threads:
            t.start()

        while True:
            try:
                streamName, line = self.q.get(block=True, timeout=timeout)
                if line:
                    if 'Failed to initialize Jenkins' in line:
                        raise FailedToStart(line)

                    if 'is fully up and running' in line:
                        log.info(line)
                        return
                else:
                    log.warn('Stream %s has terminated', streamName)

            except Queue.Empty:
                print "unexpected end!"
                break

if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger('').setLevel(logging.INFO)

    log.info("Hello!")

    jl = JenkinsLancher('/home/sal/workspace/jenkinsapi/src/jenkinsapi_tests/systests/jenkins.war')
    jl.start()
    log.info("Jenkins was launched...")

    time.sleep(30)

    log.info("...now to shut it down!")
    jl.stop()
