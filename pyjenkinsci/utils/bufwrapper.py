from cStringIO import StringIO

class bufwrapper( object ):
    """
    Basic buffer-wrapper - wraps up an output stream with a buffer.
    """
    def __init__( self, stream, buffer=None ):
        self.stream = stream

        assert hasattr( self.stream, "write" ), "%s does not support write" % repr(stream)

        if buffer is None:
            self.buf = StringIO()
        else:
            self.buf = buffer

    def get_and_clear( self ):
        """
        Get the contents of the buffer and clear it.
        """
        old_buffer = self.buf
        self.buf = StringIO()
        return old_buffer.getvalue()

    def flush( self ):
        for item in [ self.stream, self.buf ]:
            if hasattr( item, "flush" ) and callable( item.flush ):
                item.flush()


    def close(self):
        self.stream.close()

    def write(self, txt ):
        self.stream.write(txt)
        self.buf.write(txt)

    def getvalue(self):
        return self.buf.getvalue()
