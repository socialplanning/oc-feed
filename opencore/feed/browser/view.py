from Products.Five import BrowserView
from opencore.feed.interfaces import IFeedData
from topp.utils.pretty_date import prettyDate

class FeedView(BrowserView):
    """view that simply adapts context to IFeedData (as promised by
       marker interface ICanFeed), exposed as 'feed' attribute """

    def __init__(self, context, request):
        super(FeedView, self).__init__(context, request)
        self.feed = IFeedData(context)
        
    def pretty_date(self, date):
        # XXX this is copy/pasted
        return prettyDate(date)

