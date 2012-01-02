try:
    import hashlib
except ImportError:
    import md5


def new_digest():
    if hashlib:
        m = hashlib.md5()
    else:
        m = md5.new()
    return m

if __name__ == "__main__":
    x = new_digest()
    x.update("123")
    print repr( x.digest() )
