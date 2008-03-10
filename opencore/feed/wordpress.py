import feedparser
from opencore.feed.base import BaseFeedAdapter
from opencore.feed.interfaces import IFeedData
from opencore.feed.interfaces import IFeedItem
from opencore.interfaces import IProject
from zope.component import adapts
from zope.component import createObject
from zope.interface import implements

class WordpressFeedAdapter(BaseFeedAdapter):
    """feed for recent wordpress blogs"""
    # XXX this should not be used if the project has no blog

    implements(IFeedData)
    adapts(IProject)

#    @property
    def items(self, n_items=5):

        # without the trailing slash, one gets different results!
        # see http://trac.openplans.org/openplans/ticket/2197#comment:3
        uri = '%s/blog/feed/' % self.context.absolute_url()
        feed = feedparser.parse(uri)
        
        try:
            title = feed.feed.title
        except AttributeError:
            # this means the uri is not a feed (or something?)
            return

        # maybe this should be done after comments?
        # feed.entries.sort(key=date_key) # they appeared sorted already?
        feed.entries = feed.entries[:n_items]

        # sort comments to entries
        for entry in feed.entries:
            comment_feed = '%scomments/feed/' % entry.link
            comments = feedparser.parse(comment_feed)
            entry.n_comments = int(entry['slash_comments'])

#             if entry.n_comments == 1:
#                 entry.comment_string = '1 comment'
#             else:
#                 entry.comment_string = '%s comments' % entry.n_comments
                
            # annote members onto the entries
            author = entry.author
            
            title = entry.title
            pubDate = entry.date

            feed_item = createObject('opencore.feed.feeditem',
                                     entry.title,
                                     entry.summary,
                                     entry.link,
                                     entry.author,
                                     entry.date)

            yield feed_item
