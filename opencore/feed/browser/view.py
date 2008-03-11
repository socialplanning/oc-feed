from opencore.feed.interfaces import IFeedBlankSlate
from opencore.feed.interfaces import IFeedData
from opencore.feed.interfaces import IHasFeedData
from opencore.member.utils import profile_path
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from topp.utils.pretty_date import prettyDate


class FeedView(BrowserView):
    """view that simply adapts context to IFeedData
       as promised by marker interface ICanFeed"""

    def __init__(self, context, request):
        adapted = IFeedData(context)
        super(FeedView, self).__init__(adapted, request)

    def pretty_date(self, date):
        # XXX this is copy/pasted
        return prettyDate(date)

    def home(self, id):
        """
        return author home (profile) absolute url
        """
        return '%s/%s' % (self.site_url, profile_path(id))

    @property
    def site_url(self):
        portal = getToolByName(self.context.context, 
                               'portal_url')
        return portal()

class HasFeedView(FeedView):
    def __init__(self, context, request):
        adapted = IHasFeedData(context)
        super(FeedView, self).__init__(adapted, request)

class BlankSlateFeedView(FeedView):

    def __init__(self, context, request):
        adapted = IFeedBlankSlate(context)
        super(FeedView, self).__init__(adapted, request)
        if self.context.is_blank:
            self.index = ZopeTwoPageTemplateFile(self.context.blankslate)
