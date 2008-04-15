import os

from opencore.feed.browser.view import FeedView
from opencore.feed.interfaces import ITeamFeedData
from opencore.feed.interfaces import IFeedBlankSlate
from opencore.feed.listen import ListsFeedAdapter
from opencore.feed.project import WikiFeedAdapter
from opencore.feed.wordpress import WordpressFeedAdapter
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.listen.interfaces import ISearchableArchive
from zope.component import getAdapter
from zope.component import getUtility
from zope.interface import implements

class ListsFeedBlankSlate(ListsFeedAdapter):
    implements(IFeedBlankSlate)
    blankslate = 'lists_blank_slate.pt'
    @property
    def is_blank(self):
        for ml_id in self.mlists:
            mlist = self.context._getOb(ml_id)
            archive = getUtility(ISearchableArchive, context=mlist)
            if archive.getToplevelMessages():
                return False
        if self.mlists:
            self.create = os.path.join(self.context.absolute_url(), self.mlists[0], 'archive', 'new_topic')
        else:
            self.create = os.path.join(self.context.absolute_url(), 'create')
        return True

class WikiFeedBlankSlate(WikiFeedAdapter):
    implements(IFeedBlankSlate)
    blankslate = 'wiki_blank_slate.pt'
    @property
    def is_blank(self):
        cat = getToolByName(self.context, 'portal_catalog')
        brains = cat(portal_type='Document',
                     path='/'.join(self.context.getPhysicalPath()))
        if len(brains) > 1:
            return False
        histories = brains[0].getObject().getHistories()
        return len(list(histories)) < 2
    
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
