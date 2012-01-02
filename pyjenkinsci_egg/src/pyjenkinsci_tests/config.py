import os

#Disable HTTP PROXY
CLEAR_PROXY = os.environ.get("CLEAR_PROXY","")
if len( CLEAR_PROXY ) > 0:
    del os.environ["HTTP_PROXY"]

JENKINS_BASE = os.environ.get( "JENKINS_BASE", "http://localhost:8080/jenkins" )
HTTP_PROXY = os.environ.get( "HTTP_PROXY", "" )
BUILD_NAME_TEST1 = "test1"

if __name__ == "__main__":
    print( "Jenkins base: %s" % JENKINS_BASE )
    print( "Http Proxy: %s"  %HTTP_PROXY )