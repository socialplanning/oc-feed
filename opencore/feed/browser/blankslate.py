import os

from opencore.feed.browser.view import FeedView
from opencore.feed.interfaces import ITeamFeedData
from opencore.feed.interfaces import IFeedBlankSlate
from opencore.feed.listen import ListsFeedAdapter
from opencore.feed.project import WikiFeedAdapter
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from zope.interface import implements

class ListsFeedBlankSlate(ListsFeedAdapter):
    implements(IFeedBlankSlate)
    blankslate = 'lists_blank_slate.pt'

class BlankSlateTeamFeedView(FeedView):
    
    blankslate = 'team_blank_slate.pt'

    def __init__(self, context, request):
        adapted = ITeamFeedData(context)
        super(FeedView, self).__init__(adapted, request)
        self.n_members = len(context.projectMemberIds())
        if self.n_members < 2:
            self.index = ZopeTwoPageTemplateFile(self.blankslate)

    def number_of_members(self):
        if self.n_members == 1:
            return '1 member'
        return '%s members' % self.n_members
