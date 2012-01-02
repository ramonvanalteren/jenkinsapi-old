"""
Generate random IDs.
"""
import random

ID_VALID = "abcdefghijklmnopqrstuvwxyz0123456789"

def mk_id(length=5, prefix=""):
    idchars = []
    for count in range( 0, length ):
        idchars.append( random.choice( ID_VALID ) )
    return "%s%s" % ( prefix, "".join( idchars ) )

if __name__ == "__main__":
    for i in range(0, 50):
        print repr( mk_id( i ) )
