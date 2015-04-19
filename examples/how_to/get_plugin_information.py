"""
Get information about currently installed plugins
"""
from __future__ import print_function

from jenkinsapi.jenkins import Jenkins


def get_plugin_information(url, plugin_name, username=None, password=None):
    J = Jenkins(url, username, password)
    return J.get_plugins()[plugin_name]


if __name__ == '__main__':
    import pprint
    plugin = get_plugin_information('http://localhost:8080', 'subversion')
    print(repr(plugin))
    pprint.pprint(plugin.__dict__)
