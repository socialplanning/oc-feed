from BTrees.OOBTree import OOBTree
from opencore.feed import annot_key
from opencore.feed.interfaces import IFeedItem
from opencore.feed.interfaces import IFeedData
from opencore.member.utils import profile_path
from opencore.member.utils import portrait_thumb_path
from zope.app.annotation import IAnnotations
from zope.component import createObject
from zope.interface import implements
from Products.CMFCore.utils import getToolByName

import time

class BaseFeedAdapter(object):
    """Useful base class that provides most common functionality.
       Context needs to provide dublin core, and support annotations.
       XXX: this should be enforced by the adaptation contract

       Feed items are stored in annotations on the context object, as
       an OOBTree where the keys are a floating point representation
       of seconds since the epoch (python's time.time() value).  Since
       OOBTree's automatically sort by key, the feed will be ordered
       from oldest to newest.
       
       Implementations only have to provide the items iterable"""

    implements(IFeedData)

    n_items_default = 5

    def __init__(self, context):
        self.context = context
        annot = IAnnotations(self.context)
        storage = annot.get(annot_key, None)
        if storage is None:
            storage = OOBTree()
            annot[annot_key] = storage
        self.storage = storage

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

    @property
    def items(self, n_items=None):
        """
        Return the last n_items from the feed.
        """
        if n_items is None:
            n_items = self.n_items_default
        return reversed(self.storage.values()[-n_items:])

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

        # is there a reason we're using createObject and not just
        # instantiating it directly?
        feeditem = createObject('opencore.feed.feeditem', **kw)
        added = 0
        while added == 0:
            added = self.storage.insert(time.time(), feeditem)

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
