from jenkinsapi.jenkins import Jenkins
import xml.etree.ElementTree as ET

J = Jenkins('http://localhost:8080')
EMPTY_JOB_CONFIG = '''
<?xml version='1.0' encoding='UTF-8'?>
<project>
  <actions>jkkjjk</actions>
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <scm class="hudson.scm.NullSCM"/>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers class="vector"/>
  <concurrentBuild>false</concurrentBuild>
  <builders/>
  <publishers/>
  <buildWrappers/>
</project>
'''

jobname = 'foo_job'
new_job = J.create_job(jobname, EMPTY_JOB_CONFIG)
new_conf = new_job.get_config()

root = ET.fromstring(new_conf.strip())

builders = root.find('builders')
shell = ET.SubElement(builders, 'hudson.tasks.Shell')
command = ET.SubElement(shell, 'command')
command.text = "ls"

print ET.tostring(root)
J[jobname].update_config(ET.tostring(root))

#J.delete_job(jobname)

