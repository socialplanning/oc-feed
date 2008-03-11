from zope.interface import Interface
from zope.schema import ASCII
from zope.schema import Bool
from zope.schema import Datetime
from zope.schema import Iterable
from zope.schema import Text
from zope.schema import TextLine

class ICanFeed(Interface):
    """Marker interface to mean that component can create feeds"""

class IHasBlogFeed(Interface):
    """Marker interface to mean that component has feeds"""

class IHasTeamFeed(Interface):
    """Marker interface to mean that component has feeds"""

class IFeedData(Interface):
    """interface to expose necessary data for feed creation"""

    title = TextLine(title=u'Feed title',
                     description=u'Main title of the feed')
    link = ASCII(title=u'Feed link',
                 description=u'Link to the object the feed represents')
    description = Text(title=u'Feed description',
                       description=u'Description of the feed')
    language = TextLine(title=u'Feed language',
                        description=u'Language of the feed')
    pubDate = Datetime(title=u'Feed date',
                       description=u'Date that the feed was last updated')
    author = TextLine(title=u'Feed author',
                      description=u'Author of the feed')
    items = Iterable(title=u'Feed items',
                     description=u'Items the feed is providing')

class IBlogFeedData(IFeedData):
    """marker interface so that projects can have multiple feeds"""

class ITeamFeedData(IFeedData):
    """marker interface so that projects can have multiple feeds"""

class IFeedBlankSlate(IFeedData):
    """interface for feeds with a blank-slate template"""
    blankslate = TextLine(title=u'Blank slate',
                          description=u'Name of the page template file')
    is_blank = Bool(title=u'is blank?',
                    description=u'whether the feed is blank or not')
    

class IFeedItem(Interface):
    """interface that each feed item should implement"""

    title = TextLine(title=u'Feed item title',
                     description=u'Main title of feed item')
    link = ASCII(title=u'Feed item link',
                 description=u'Link to the feed item')
    description = Text(title=u'Feed item description',
                       description=u'Description of the feed item')
    pubDate = Datetime(title=u'Feed item date',
                       description=u'Date updated for the feed item')
    body = Text(title=u'Feed item body',
                description=u'Body of the feed item, if any',
                default=u'',
                required=False)
