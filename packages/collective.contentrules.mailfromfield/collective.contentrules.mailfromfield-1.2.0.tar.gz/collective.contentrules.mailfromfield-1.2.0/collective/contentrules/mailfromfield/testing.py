# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import (
    FunctionalTesting,
    IntegrationTesting,
    MOCK_MAILHOST_FIXTURE,
    PloneSandboxLayer,
)

import collective.contentrules
import plone.app.contentrules


class CollectiveContentrulesMailfromfieldLayer(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML("testing.zcml", package=plone.app.contentrules.tests)
        self.loadZCML(package=collective.contentrules.mailfromfield)


CONTENTRULES_FIXTURE = CollectiveContentrulesMailfromfieldLayer()


CONTENTRULES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CONTENTRULES_FIXTURE, MOCK_MAILHOST_FIXTURE),
    name="CollectiveContentrulesMailfromfieldLayer:IntegrationTesting",
)


CONTENTRULES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CONTENTRULES_FIXTURE,),
    name="CollectiveContentrulesMailfromfieldLayer:FunctionalTesting",
)
