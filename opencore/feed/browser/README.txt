Verify that for all objects that should provide rss
a view can be obtained::

    >>> from zope.component import getMultiAdapter
    >>> request = self.portal.REQUEST

Project::
    >>> proj = self.portal.projects.p1
    >>> view = getMultiAdapter((self.portal.projects.p1, request), name='rss')
    >>> html = view()

Projects::
# Projects folder needs to be marked during setup with ICanFeed first
#    >>> view = getMultiAdapter((self.portal.projects, request), name='rss')
#    >>> html = view()

People::
# People folder needs to be marked during setup with ICanFeed first
#    >>> view = getMultiAdapter((self.portal.people, request), name='rss')
#    >>> html = view()

Page::
    >>> view = getMultiAdapter((self.portal.projects.p1._getOb('project-home'),
    ...                         request),
    ...                         name='rss')
    >>> html = view()

Mailing Lists::

First need to create a mailing list on a project::
    >>> self.login('m3')
    >>> proj = self.portal.projects.p1
    >>> from topp.featurelets.interfaces import IFeatureletSupporter
    >>> fs = IFeatureletSupporter(proj)
    >>> from opencore.listen.featurelet import ListenFeaturelet
    >>> fs.installFeaturelet(ListenFeaturelet(fs))

Now that we have a lists folder, it should provide an rss view::
     >>> lf = self.portal.projects.p1.lists

# Code needs to be added to listen featurelet creation that marks the list
# folder with ICanFeed first
#    >>> view = getMultiAdapter((lf, request), name='rss')
#    >>> html = view()

    >>> view = getMultiAdapter((lf._getOb('p1-discussion'),
    ...                         request),
    ...                         name='rss')
    >>> html = view()
