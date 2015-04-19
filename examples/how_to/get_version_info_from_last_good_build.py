"""
Extract version information from the latest build.
"""
from __future__ import print_function

from jenkinsapi.jenkins import Jenkins


def get_scm_info_from_latest_good_build(
        url, jobName, username=None, password=None):
    J = Jenkins(url, username, password)
    job = J[jobName]
    lgb = job.get_last_good_build()
    return lgb.get_revision()

if __name__ == '__main__':
    print(
        get_scm_info_from_latest_good_build(
            'http://localhost:8080',
            'fooJob'))
