from ftw.zipexport.interfaces import IContainerZippedEvent
from ftw.zipexport.interfaces import IItemZippedEvent
from zope.interface import implementer


@implementer(IContainerZippedEvent)
class ContainerZippedEvent(object):

    def __init__(self, obj, comment=None, action=None, actor=None, time=None):
        self.object = obj
        self.action = action
        self.comment = comment
        self.actor = actor
        self.time = time


@implementer(IItemZippedEvent)
class ItemZippedEvent(object):

    def __init__(self, obj, comment=None, action=None, actor=None, time=None):
        self.object = obj
        self.action = action
        self.comment = comment
        self.actor = actor
        self.time = time
