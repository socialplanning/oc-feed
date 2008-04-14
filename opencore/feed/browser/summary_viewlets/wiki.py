from Products.Five.viewlet.viewlet import ViewletBase

class WikiSummaryViewlet(ViewletBase):

    sort_order = 300

    def render(self):
        view = self.context.restrictedTraverse('blank-slate-feed')
        return view()
