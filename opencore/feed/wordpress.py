import feedparser
from opencore.feed.base import BaseFeedAdapter

class WordpressFeedAdapter(BaseFeedAdapter):
    """feed for recent wordpress blogs"""
    # XXX this should not be used if the project has no blog

    implements(IFeedData)
    adapts(IProject)

    def __init__(self, context):
        BaseFeedAdapter(self, context)
        
        # without the trailing slash, one gets different results!
        # see http://trac.openplans.org/openplans/ticket/2197#comment:3
        uri = '%s/blog/feed/' % context.absolute_url()
        feed = feedparser.parse(uri)


    @property
    def items(self, n_items=5):
        
        try:
            title = feed.feed.title
        except AttributeError:
            # this means the uri is not a feed (or something?)
            return

        # maybe this should be done after comments?
        # feed.entries.sort(key=date_key) # they appeared sorted already?
        feed.entries = feed.entries[:n]

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
            membrane_tool = self.get_tool('membrane_tool')
            for entry in feed.entries:
                members = membrane_tool(getId=entry.author)
                if len(members) == 1:
                    entry.member = members[0].getObject() # XXX necessary to keep track of these?

                else:
                    entry.member = None

            yield entry # no! bad!
