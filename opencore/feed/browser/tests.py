from opencore.account import utils
utils.turn_confirmation_on()
from opencore.testing import dtfactory as dtf
from opencore.testing import setup as oc_setup
from opencore.testing.layer import OpencoreContent
from zope.app.component.hooks import setSite, setHooks
from zope.testing import doctest
import unittest

optionflags = doctest.ELLIPSIS

import warnings; warnings.filterwarnings("ignore")

def test_suite():
    from Products.CMFCore.utils import getToolByName
    from Products.Five.utilities.marker import erase as noLongerProvides
    from Products.PloneTestCase import setup
    from Products.PloneTestCase.PloneTestCase import FunctionalTestCase
    from Testing.ZopeTestCase import installProduct
    from opencore.interfaces.workflow import IReadWorkflowPolicySupport
    from opencore.listen.featurelet import ListenFeaturelet
    from opencore.nui.indexing import authenticated_memberid
    from opencore.testing import utils
    from pprint import pprint
    from topp.featurelets.interfaces import IFeatureletSupporter
    from zope.component import getUtility
    from zope.interface import alsoProvides
    import pdb
        
    setup.setupPloneSite()

    def readme_setup(tc):
        oc_setup.fresh_skin(tc)
        setSite(tc.portal)
        setHooks()

    globs = locals()
    readme = dtf.ZopeDocFileSuite("README.txt", 
                                  optionflags=optionflags,
                                  package='opencore.feed.browser',
                                  test_class=FunctionalTestCase,
                                  globs = globs,
                                  setUp=readme_setup,
                                  layer = OpencoreContent                                       
                                  )

    return unittest.TestSuite((readme,))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
