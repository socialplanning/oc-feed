from Products.Five import BrowserView
from topp.utils.pretty_date import prettyDate

class FeedView(BrowserView):
    """view that simply adapts context to IFeedData
       as promised by marker interface ICanFeed"""

    def pretty_date(self, date):
        # XXX this is copy/pasted
        return prettyDate(date)

