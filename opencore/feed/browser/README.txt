-*- mode: doctest ;-*-

Verify that for all objects that should provide rss
a view can be obtained::

    >>> from zope.component import getMultiAdapter
    >>> request = self.portal.REQUEST

Project::
    >>> proj = self.portal.projects.p1
    >>> view = proj.restrictedTraverse('@@rss')
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
    >>> page = proj._getOb('project-home')
    >>> view = page.restrictedTraverse('@@rss')
    >>> html = view()

Mailing Lists::

First need to create a mailing list on a project::
    >>> self.login('m3')
    >>> from topp.featurelets.interfaces import IFeatureletSupporter
    >>> fs = IFeatureletSupporter(proj)
    >>> from opencore.listen.featurelet import ListenFeaturelet
    >>> fs.installFeaturelet(ListenFeaturelet(fs))

Now that we have a lists folder, it should provide an rss view::
     >>> lf = proj.lists

# Code needs to be added to listen featurelet creation that marks the list
# folder with ICanFeed first
#    >>> view = getMultiAdapter((lf, request), name='rss')
#    >>> html = view()

    >>> mlist = lf._getOb('p1-discussion')
    >>> view = mlist.restrictedTraverse('@@rss')
    >>> html = view()
