from ftw.zipexport.interfaces import IZipRepresentation
from zope.component import adapts
from zope.interface import implementer
from zope.interface import Interface


@implementer(IZipRepresentation)
class NullZipRepresentation(object):
    """
    defualt zip export implementation
    """
    adapts(Interface, Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_files(self, path_prefix=u"", recursive=True, toplevel=True):
        return []
