from opencore.feed.base import BaseFeedAdapter
from opencore.feed.interfaces import IFeedData
from opencore.feed.interfaces import IFeedItem
from opencore.interfaces import IOpenTeam
from opencore.interfaces import IProject
from opencore.member.utils import profile_path
from Products.CMFCore.utils import getToolByName
from topp.utils.pretty_date import prettyDate
from zope.component import adapts
from zope.component import getUtility
from zope.component import createObject
from zope.interface import alsoProvides
from zope.interface import implements

class TeamFeedAdapter(BaseFeedAdapter):
    implements(IFeedData)
    adapts(IProject)

    title = 'Team'
    
    @property
    def link(self):
        return '%s/team' % self.context.absolute_url()

    @property
    def items(self, n_items=12):
        
        # TODO: sorting

        for member in self.context.projectMembers():
            link = profile_path(member.id)
            feed_item = createObject('opencore.feed.feeditem',
                                     member.id,
                                     member.fullname,
                                     link,
                                     member.id,
                                     member.Date())

            yield feed_item
