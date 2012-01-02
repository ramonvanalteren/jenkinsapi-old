from setuptools import setup, find_packages

GLOBAL_ENTRY_POINTS = {
        "console_scripts":[ "jenkins_invoke=pyhudson.command_line.hudson_invoke:main",
                            "meta_test=pyhudson.command_line.meta_test:main", ] }

setup(name='pyjenkinsci',
      version='0.0.35',
      description='A Python API for accessing resources a Hudson or Jenkins continuous-integration server.',
      author='Salim Fadhley',
      author_email='sal@stodge.org',
      #install_requires = [ 'elementtree>=1.2-20040618' ],
      #tests = "tests",
      package_dir = {'':'src'},
      packages=find_packages('src'),
      zip_safe=True,
      include_package_data = False,
      entry_points = GLOBAL_ENTRY_POINTS,
      )
