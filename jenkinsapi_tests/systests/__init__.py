import os
from jenkinsapi_utils.jenkins_launcher import JenkinsLancher


launcher = None


def setUpPackage():
    global launcher
    import ipdb
    ipdb.set_trace()

    systests_dir, _ = os.path.split(__file__)
    war_path = os.path.join(systests_dir, 'jenkins.war' )
    launcher = JenkinsLancher(war_path)
    launcher.start()


def tearDownPackage():
    launcher.stop()
