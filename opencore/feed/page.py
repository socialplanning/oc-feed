from Products.CMFCore.utils import getToolByName
from opencore.interfaces import IOpenPage
from opencore.feed.base import BaseFeedAdapter
from opencore.feed.interfaces import IFeedData
from opencore.feed.interfaces import IFeedItem
from zope.component import adapts
from zope.component import createObject
from zope.interface import alsoProvides
from zope.interface import implements

class PageFeedAdapter(BaseFeedAdapter):
    """feed for wiki page modifications"""
    
    implements(IFeedData)
    adapts(IOpenPage)

    @property
    def items(self):
        pr = getToolByName(self.context, 'portal_repository')
        items = []
        for version in pr.getHistory(self.context, countPurged=False):
            description = version.comment
            page = version.object
            title = page.Title()
            link = page.absolute_url()
            pubDate = page.modified()
            author = version.sys_metadata.get('principal')
            #body = page.getText()
            feed_item = createObject('opencore.feed.feeditem',
                                     title,
                                     description,
                                     link,
                                     author,
                                     pubDate)
            items.append(feed_item)
        return items
