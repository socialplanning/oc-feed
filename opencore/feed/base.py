from opencore.feed.interfaces import IFeedItem
from zope.interface import implements

class BaseFeedAdapter(object):
    """Useful base class that provides most common functionality.
       Context needs to provide dublin core.

       Implementations only have to provide the items iterable"""

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return '%s Opencore Feed' % self.context.Title()

    @property
    def description(self):
        return 'Opencore Feed for %s: %s' % (self.context.Title(),
                                             self.context.Description())

    @property
    def link(self):
        return self.context.absolute_url()

    language = 'en-us'

    @property
    def pubDate(self):
        return self.context.modified()

    @property
    def author(self):
        return self.context.Creator()

class FeedItem(object):
    implements(IFeedItem)

    def __init__(self, title, description, link, author, pubDate, body=None, context=None, byline=None):
        self.title = title
        self.description = description
        self.link = link
        self.author = author
        self.pubDate = pubDate
        if body is None:
            self.body = u''
        else:
            self.body = body
        if context:
            self.context = context
        if byline:
            self.byline = byline
