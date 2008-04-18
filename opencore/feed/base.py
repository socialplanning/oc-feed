from opencore.feed.interfaces import IFeedItem
from opencore.member.utils import profile_path
from opencore.member.utils import portrait_thumb_path
from zope.component import createObject
from zope.interface import implements
from Products.CMFCore.utils import getToolByName

class BaseFeedAdapter(object):
    """Useful base class that provides most common functionality.
       Context needs to provide dublin core.

       Implementations only have to provide the items iterable"""

    def __init__(self, context):
        self.context = context

    # XXX this should become full_title, title should be short
    @property
    def title(self):
        return '%s Opencore Feed' % self.context.Title()

    @property
    def itemstitle(self):
        return self.title.lower()

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

    def add_item(self, **kw):
        """Adds an item to the list of items maintained by this adapter.  The
        following arguments are required: %r""" % IFeedItem.names()
        for requirement, description in IFeedItem.namesAndDescriptions():
            if description.required and requirement not in kw:
                raise NameError("%s is a required argument to this method." %
                requirement)

        if not 'authorURL' in kw or not kw['authorURL']:
            kw['authorURL'] = self.memberURL(kw['author'])

        if not 'logo' in kw or not kw['logo']:
            kw['logo'] = self.member_portraitURL(kw['author'])

        if not hasattr(self,'_items'):
            self._items = []

        self._items.append(createObject('opencore.feed.feeditem',**kw))

    def memberURL(self, id):
        """Utility method that uses the current context to convert a member id
        into a URL"""
        return '%s/%s' % (getToolByName(self.context, 'portal_url')(),
                          profile_path(id))

    def member_portraitURL(self, id):
        """
        utility method that provides a URL to a member's portrait thumbnail
        """
        return '%s/%s' % (getToolByName(self.context, 'portal_url')(),
                          portrait_thumb_path(id))

class AggreateFeedAdapter(BaseFeedAdapter):
    """
    aggregates feeds from several sources and puts them together sorted by date
    """

    def subfeeds(self):
        """subclasses should implement this method to define their subfeeds"""
        return []

class FeedItem(object):
    implements(IFeedItem)

    def __init__(self, title, description, link, author, pubDate, body=None, context=None, byline=None, responses=None, authorURL=None, logo=None):
        """
        * context: dictionary containing { 'title':, 'link': of the appropriate context
        * replies: should be FeedItemReplies instance
        """

        self.title = title
        self.description = description
        self.link = link
        self.author = author
        self.authorURL = authorURL
        if logo:
            self.logo = logo
        self.pubDate = pubDate
        if body is None:
            self.body = u''
        else:
            self.body = body
        if context:
            self.context = context
        if byline:
            self.byline = byline
        if responses:
            self.responses = responses

     
class FeedItemResponses(object):
    def __init__(self, number, link, name=None, plural=None):
        self.number = number
        self.link = link
        if name is None:
            self.name = 'reply'
            self.plural = 'replies'
        else:
            self.name = name
            if plural is None:
                self.plural = '%ss' % name
        
    def reply_string(self):
        if self.number == 1:
            return '%s %s' % (self.number, self.name)
        else:
            return '%s %s' % (self.number, self.plural)
