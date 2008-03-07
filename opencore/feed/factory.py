from zope.component.factory import Factory
from opencore.feed.base import FeedItem

feedItemFactory = Factory(
    FeedItem,
    title=u'Create a new feed item',
    description=u'This factory instantiates new feed items.')
