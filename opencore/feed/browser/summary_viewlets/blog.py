from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from opencore.browser.blankslate import BlankSlateViewlet
import opencore.feed.browser
import os

class BlogSummaryViewlet(BlankSlateViewlet):
    blank_template = ZopeTwoPageTemplateFile('blog_blank_slate.pt')
    template = os.path.join(os.path.dirname(opencore.feed.browser.__file__), 'feed_snippet.pt')
    template = ZopeTwoPageTemplateFile(template)
    adapter_name = 'blog'

    sort_order = 100

    def is_blank(self):
        no_content = not self.context.items
        can_add_content = self.context.context.isProjectMember()
        return (no_content and can_add_content)
