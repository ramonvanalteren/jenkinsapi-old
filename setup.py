from setuptools import setup, find_packages

GLOBAL_ENTRY_POINTS = {
        "console_scripts":[ "jenkins_invoke=jenkinsapi.command_line.jenkins_invoke:main"]
        }

setup(name='jenkinsapi',
      version='0.1',
      description='A Python API for accessing resources on a Jenkins continuous-integration server.',
      author="Ramon van Alteren",
      author_email='ramon@vanalteren.nl',
      package_dir = {'':'jenkinsapi'},
      packages=find_packages('jenkinsapi'),
      zip_safe=True,
      include_package_data = False,
      entry_points = GLOBAL_ENTRY_POINTS,
      url="https://github.com/ramonvanalteren/jenkinsapi",
      )
