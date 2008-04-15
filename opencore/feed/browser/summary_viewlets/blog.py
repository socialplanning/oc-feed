from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from opencore.browser.blankslate import BlankSlateViewlet
from opencore.member.utils import portrait_thumb_path
from opencore.member.utils import profile_path
from topp.utils.pretty_date import prettyDate
from zope.formlib.namedtemplate import NamedTemplate
from zope.component import getAdapter
import opencore.feed.browser
import os

class BlogSummaryViewlet(BlankSlateViewlet):
    blank_template = ZopeTwoPageTemplateFile('blog_blank_slate.pt')
    template = os.path.join(os.path.dirname(opencore.feed.browser.__file__), 'portrait_feed_snippet.pt')
    template = ZopeTwoPageTemplateFile(template)
    adapter_name = 'blog'

    sort_order = 100

    def is_blank(self):
        return (not list(self.context.items) and
                self.context.context.isProjectMember())

    def pretty_date(self, date):
        # XXX this is copy/pasted
        return prettyDate(date)

    def home(self, id):
        """return author home (profile) absolute url"""
        return '%s/%s' % (getToolByName(self.context.context, 'portal_url')(),
                          profile_path(id))

    def portrait(self, id):
        """return author portrait thumb absolute url"""
        return '%s/%s' % (self.site_url, portrait_thumb_path(id))
