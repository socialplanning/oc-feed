from Products.Five.viewlet.viewlet import ViewletBase

class DiscussionsSummaryViewlet(ViewletBase):

    sort_order = 200

    def render(self):
        view = self.context.restrictedTraverse('lists/blank-slate-feed')
        return view()
