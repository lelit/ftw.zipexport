from ftw.zipexport.interfaces import IZipRepresentation
from ftw.zipexport.representations.general import NullZipRepresentation
from plone.namedfile.interfaces import INamedFileField
from plone.rfc822.interfaces import IPrimaryFieldInfo
from plone.dexterity.interfaces import IDexterityItem
from zope.component import adapts
from zope.component import getAdapter
from zope.interface import implements
from zope.interface import Interface
from StringIO import StringIO

from plone.namedfile.interfaces import HAVE_BLOBS
if HAVE_BLOBS:
    from plone.namedfile.interfaces import INamedBlobFile


class DexterityItemZipRepresentation(NullZipRepresentation):
    implements(IZipRepresentation)
    adapts(IDexterityItem, Interface)

    def get_files(self, path_prefix="", recursive=True, toplevel=True):
        try:
            primary_adapter = getAdapter(self.context,
                                         interface=IPrimaryFieldInfo)
        except TypeError:
            # if no primary field is available PrimaryFieldInfo Adapter throws TypeError
            return

        if INamedFileField.providedBy(primary_adapter.field):
            named_file = primary_adapter.value
            if primary_adapter.value:
                yield self.get_file_tuple(named_file, path_prefix)

    def get_file_tuple(self, named_file, path_prefix):
        if HAVE_BLOBS and INamedBlobFile.providedBy(named_file):
            return (path_prefix + "/" + named_file.filename, named_file.open())
        else:
            stream_data = StringIO(named_file.data)
            return (path_prefix + "/" + named_file.filename, stream_data)
