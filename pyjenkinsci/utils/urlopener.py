import urllib2

import logging

log = logging.getLogger( __name__ )

DEFAULT_PROXYPORT = 80
DEFAULT_PROXY_PASS = "Research123"
DEFAULT_PROXY_USER = "wsa_oblicqs_dev"

def mkurlopener( proxyhost, proxyport, proxyuser, proxypass ):
    if not proxyhost:
        return urllib2.urlopen
    else:
        if proxyport is None:
            proxyport = DEFAULT_PROXYPORT

        if proxypass is None:
            proxypass = DEFAULT_PROXY_PASS

        if proxyuser is None:
            proxyuser = DEFAULT_PROXY_USER

        assert type( proxyport ) == int, "Proxy port should be an int, got %s" % repr( proxyport )
        assert type( proxypass ) == str, "Proxy password should be a sting, got %s" % repr( proxypass )
        assert type( proxyuser ) == str, "Proxy username should be a string, got %s" % repr( proxyuser )

        proxy_spec = { 'http': 'http://%s:%i/' % (proxyhost, proxyport),
                       'https': 'http://%s:%i/' % (proxyhost, proxyport) }

        proxy_handler = urllib2.ProxyHandler( proxy_spec )
        proxy_auth_handler = urllib2.HTTPBasicAuthHandler()
        proxy_auth_handler.add_password( None, proxyhost, proxyuser, proxypass )

        opener = urllib2.build_opener(proxy_handler, proxy_auth_handler)

        return opener.open
