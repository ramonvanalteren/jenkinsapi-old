"""
Get information about currently installed plugins
"""
from __future__ import print_function

from jenkinsapi.jenkins import Jenkins


def getPluinInformation(url, pluginName, username=None, password=None):
    J = Jenkins(url, username, password)
    return J.get_plugins()[pluginName]
    

if __name__ == '__main__':
    import pprint
    
    plugin = getPluinInformation('http://localhost:8080', 'subversion')
    print(repr(plugin))
    pprint.pprint(plugin.__dict__)
