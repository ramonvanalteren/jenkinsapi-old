from setuptools import setup, find_packages

GLOBAL_ENTRY_POINTS = {
        "console_scripts":[ "jenkins_invoke=pyjenkinsci.command_line.hudson_invoke:main",
                            "meta_test=pyjenkinsci.command_line.meta_test:main", ] }

setup(name='pyjenkinsci',
      version='0.0.35.1',
      description='A Python API for accessing resources on a Jenkins continuous-integration server.',
      author='Salim Fadhley',
      author_email='sal@stodge.org',
      package_dir = {'':'pyjenkinsci'},
      packages=find_packages('pyjenkinsci'),
      zip_safe=True,
      include_package_data = False,
      entry_points = GLOBAL_ENTRY_POINTS,
      url="https://github.com/ramonvanalteren/pyjenkinsci",
      )
