from Products.Five.viewlet.viewlet import ViewletBase

class BlogSummaryViewlet(ViewletBase):

    sort_order = 100

    def render(self):
        view = self.context.restrictedTraverse('blogfeed')
        return view()
