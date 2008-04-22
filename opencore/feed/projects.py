from Products.CMFCore.utils import getToolByName
from opencore.interfaces.adding import IAddProject
from opencore.interfaces import IProject
from opencore.feed.base import BaseFeedAdapter
from opencore.feed.interfaces import IFeedData
from opencore.feed.interfaces import IFeedItem
from zope.component import adapts
from zope.component import createObject
from zope.interface import alsoProvides
from zope.interface import implements

class ProjectsFeedAdapter(BaseFeedAdapter):
    """feed for new projects"""
    
    implements(IFeedData)
    adapts(IAddProject)

    @property
    def items(self, n_items=10):
        if hasattr(self,'_items'):
            # If the property already contains something, there's no need to
            # regenerate it.
            return self._items

        cat = getToolByName(self.context, 'portal_catalog')
        #XXX put in max depth 1 to not search subfolders
        for brain in cat(portal_type='OpenProject',
                              sort_on='created',
                              sort_order='descending',
                              sort_limit=n_items):

            title = brain.Title
            description = brain.Description
            link = brain.getURL()
            author = brain.lastModifiedAuthor
            pubDate = brain.created

            self.add_item(title=title,
                          description=description,
                          link=link,
                          author=author,
                          pubDate=pubDate)
        return self._items
