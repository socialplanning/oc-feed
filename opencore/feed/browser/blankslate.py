from opencore.feed.interfaces import IFeedBlankSlate
from opencore.feed.project import WikiFeedAdapter
from opencore.feed.listen import ListsFeedAdapter
from Products.CMFCore.utils import getToolByName
from Products.listen.interfaces import ISearchableArchive
from zope.component import getUtility
from zope.interface import implements

class ListsFeedBlankSlate(ListsFeedAdapter):
    implements(IFeedBlankSlate)

    blankslate = 'lists_blank_slate.pt'
    @property
    def is_blank(self):
        for ml_id in self.mlists:
            mlist = self.context._getOb(ml_id)
            archive = getUtility(ISearchableArchive, context=mlist)
            if archive.getToplevelMessages():
                return False
        return True

class WikiFeedBlankSlate(WikiFeedAdapter):
    implements(IFeedBlankSlate)

    blankslate = 'wiki_blank_slate.pt'
    @property
    def is_blank(self):
        cat = getToolByName(self.context, 'portal_catalog')
        brains = cat(portal_type='Document',
                     path='/'.join(self.context.getPhysicalPath()))
        if len(brains) > 1:
            return False
        histories = brains[0].getObject().getHistories()
        return len(list(histories)) < 2
