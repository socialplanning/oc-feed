from Products.CMFCore.utils import getToolByName
from opencore.configuration import DEFAULT_ROLES
from opencore.interfaces.adding import IAddProject
from opencore.interfaces import IProject
from opencore.feed.base import BaseFeedAdapter
from opencore.feed.interfaces import IFeedData
from opencore.feed.interfaces import IFeedItem
from zope.component import adapts
from zope.component import createObject
from zope.interface import alsoProvides
from zope.interface import implements

class WikiFeedAdapter(BaseFeedAdapter):
    """feed for wiki page modifications in project
       XXX or should this be only for new pages?
       probably want this to be across all changes within the project
       including all featurelets
       maybe then we iterate through the feed across all featurelets,
       parse them, and aggregate with latest pages"""
    
    implements(IFeedData)
    adapts(IProject)

    title = 'Pages'

    def is_project_admin(self):
        """
        Boolean method for checking if the current user
        is a team manager of the adapted project. It seems
        we can't let the project itself reach the publisher(?)
        because it's not acquisition-wrapped. i think this is
        because the template isn't really bound to a proper view
        though i'm not quite sure either how this implementation
        works or whether this is really the cause of the problem.

        (maybe we should set __of__ manually in initialization?)
        """
        project = self.context
        team = project.getTeams()[0]
        membertool = getToolByName(project, 'portal_membership')
        mem_id = membertool.getAuthenticatedMember().getId()
        return team.getHighestTeamRoleForMember(mem_id) == DEFAULT_ROLES[-1]

    @property
    def link(self):
        # XXX this will become '%s/home'
        # how to get this?
        return '%s/project-home' % self.context.absolute_url()

    @property
    def items(self, n_items=5):
        cat = getToolByName(self.context, 'portal_catalog')
        for brain in cat(portal_type='Document',
                         path='/'.join(self.context.getPhysicalPath()),
                         sort_on='modified',
                         sort_order='descending',
                         sort_limit=n_items):

            title = brain.Title
            #XXX would be nice if the description was the revision note
            #we should index it that way
            description = brain.Description
            author = brain.lastModifiedAuthor
            link = brain.getURL()
            pubDate = brain.modified
            #XXX maybe we should stick the body in here as well?
            # the feed supports passing the "body" attribute
            # problem though, is that we don't want to put all of it in there
            # and if we cut it off, we might cut off some html
            # let's just leave it off for now
            #body = brain.getObject().getText()

            feed_item = createObject('opencore.feed.feeditem',
                                     title,
                                     description,
                                     link,
                                     author,
                                     pubDate)
            yield feed_item
