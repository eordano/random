
class FileNode:
    def __init__(self, name="", url="", parent=None, path=None):
        self.name = name
        self.url = url
        self.parent = parent
        self.path = path

    def __unicode__(self):
        return u'file %s'%self.name

    def __repr__(self):
        return self.__unicode__().encode('iso-8859-1')

