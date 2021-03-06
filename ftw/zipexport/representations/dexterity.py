from ftw.zipexport.events import ItemZippedEvent
from ftw.zipexport.interfaces import IZipRepresentation
from ftw.zipexport.representations.general import NullZipRepresentation
from plone import api
from plone.dexterity.interfaces import IDexterityContainer, IDexterityItem
from plone.namedfile.interfaces import INamedField
from plone.rfc822.interfaces import IPrimaryFieldInfo
from Products.CMFPlone.utils import safe_unicode
from io import BytesIO
from zope.component import adapts
from zope.component import getAdapter, getMultiAdapter
from zope.event import notify
from zope.interface import implementer
from zope.interface import Interface

from plone.namedfile.interfaces import HAVE_BLOBS
if HAVE_BLOBS:
    from plone.namedfile.interfaces import IBlobby


@implementer(IZipRepresentation)
class DexterityItemZipRepresentation(NullZipRepresentation):
    adapts(IDexterityItem, Interface)

    def get_files(self, path_prefix=u"", recursive=True, toplevel=True):
        try:
            primary_adapter = getAdapter(self.context,
                                         interface=IPrimaryFieldInfo)
        except TypeError:
            # if no primary field is available PrimaryFieldInfo
            # Adapter throws TypeError
            return

        if INamedField.providedBy(primary_adapter.field):
            named_file = primary_adapter.value
            if primary_adapter.value:
                notify(ItemZippedEvent(self.context))
                yield self.get_file_tuple(named_file, path_prefix)

    def get_file_tuple(self, named_file, path_prefix):
        path = u'{0}/{1}'.format(safe_unicode(path_prefix),
                                 safe_unicode(named_file.filename))
        if HAVE_BLOBS and IBlobby.providedBy(named_file):
            return (path, named_file.open())
        else:
            return (path, BytesIO(named_file.data))


@implementer(IZipRepresentation)
class DexterityContainerZipRepresentation(NullZipRepresentation):
    adapts(IDexterityContainer, Interface)

    def get_files(self, path_prefix="", recursive=True, toplevel=True):
        if not recursive:
            return

        if not toplevel:
            if getattr(self.context, 'zipexport_title', None):
                title = safe_unicode(self.context.zipexport_title)
            else:
                title = safe_unicode(self.context.Title())
            path_prefix = '{0}/{1}'.format(safe_unicode(path_prefix), title)

        brains = api.content.find(self.context, depth=1)
        if not brains:
            # Create an empty folder
            yield (path_prefix, None)

        for brain in brains:
            adapt = getMultiAdapter((brain.getObject(), self.request),
                                    interface=IZipRepresentation)

            for item in adapt.get_files(path_prefix=path_prefix,
                                        recursive=recursive,
                                        toplevel=False):
                yield item
