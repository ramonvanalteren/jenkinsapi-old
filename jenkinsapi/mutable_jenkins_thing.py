import urlparse

class MutableJenkinsThing(object):
    """
    """
    def get_delete_url(self):
        return '%s/doDelete' % self.baseurl

    def get_rename_url(self):
        return '%s/doRename' % self.baseurl
