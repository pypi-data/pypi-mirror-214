# -*- coding: UTF-8 -*-
from collective.contentrules.mailfromfield.actions.mail import (
    MailFromFieldAction,
    MailFromFieldAddForm,
    MailFromFieldEditForm,
)
from collective.contentrules.mailfromfield.testing import (
    CONTENTRULES_INTEGRATION_TESTING,
)
from plone import api
from plone.app.contentrules.rule import Rule
from plone.app.contentrules.tests.base import ContentRulesTestCase
from plone.app.testing import SITE_OWNER_NAME
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IExecutable, IRuleAction
from plone.testing.zope import login
from zope.component import getMultiAdapter, getUtility
from zope.interface.interfaces import IObjectEvent
from zope.interface import implementer


# basic test structure copied from plone.app.contentrules test_action_mail.py


@implementer(IObjectEvent)
class DummyEvent(object):
    def __init__(self, object):
        self.object = object


class TestMailAction(ContentRulesTestCase):
    layer = CONTENTRULES_INTEGRATION_TESTING
    maxDiff = None

    def setUp(self):
        super(TestMailAction, self).setUp()
        self.app = self.layer["app"]
        self.mailhost = self.layer["portal"].MailHost
        self.folder.setTitle("Càrtella")
        self.folder.d1.setTitle("Dòcumento")

    # BBB
    def loginAsPortalOwner(self, userName=SITE_OWNER_NAME):
        """Log in to the portal as the user who created it."""
        login(self.app["acl_users"], userName)

    def testRegistered(self):
        element = getUtility(IRuleAction, name="plone.actions.MailFromField")
        self.assertEquals("plone.actions.MailFromField", element.addview)
        self.assertEquals("edit", element.editview)
        self.assertEquals(None, element.for_)
        self.assertEquals(IObjectEvent, element.event)

    def testInvokeAddView(self):
        element = getUtility(IRuleAction, name="plone.actions.MailFromField")
        storage = getUtility(IRuleStorage)
        storage["foo"] = Rule()
        rule = self.portal.restrictedTraverse("++rule++foo")

        adding = getMultiAdapter((rule, self.portal.REQUEST), name="+action")
        addview = getMultiAdapter((adding, self.portal.REQUEST), name=element.addview)
        self.failUnless(isinstance(addview.form_instance, MailFromFieldAddForm))

        addview.form_instance.createAndAdd(
            data={
                "subject": "My Subject",
                "source": "foo@bar.be",
                "fieldName": "foo",
                "target": "object",
                "message": "Hey, Oh!",
            }
        )

        e = rule.actions[0]
        self.failUnless(isinstance(e, MailFromFieldAction))
        # TODO
        # self.assertEquals("My Subject", e.subject)
        # self.assertEquals("foo@bar.be", e.source)
        # self.assertEquals("foo", e.fieldName)
        # self.assertEquals("object", e.target)
        # self.assertEquals("Hey, Oh!", e.message)

    def testInvokeEditView(self):
        element = getUtility(IRuleAction, name="plone.actions.MailFromField")
        e = MailFromFieldAction()
        editview = getMultiAdapter((e, self.folder.REQUEST), name=element.editview)
        self.failUnless(isinstance(editview.form_instance, MailFromFieldEditForm))

    def testExecuteNoSource(self):
        self.loginAsPortalOwner()
        e = MailFromFieldAction()
        e.message = "Document created !"
        e.fieldName = "foo_attr"
        e.target = "object"
        e.subject = "Subject"
        self.folder.foo_attr = "member1@dummy.org"
        email_from_address = api.portal.get_registry_record("plone.email_from_address")
        email_from_name = api.portal.get_registry_record("plone.email_from_name")
        api.portal.set_registry_record("plone.email_from_address", "")
        ex = getMultiAdapter((self.folder, e, DummyEvent(self.folder.d1)), IExecutable)
        self.assertRaises(ValueError, ex)
        # if we provide a site mail address this won't fail anymore
        api.portal.set_registry_record("plone.email_from_address", "manager@portal.be")
        api.portal.set_registry_record("plone.email_from_name", "The Big Boss")
        ex()
        mailSent = self.mailhost.messages[0]
        self.assertIn(b'Content-Type: text/plain; charset="utf-8"', mailSent)
        self.assertIn(b"To: member1@dummy.org", mailSent)
        self.assertIn(b"From: The Big Boss <manager@portal.be>", mailSent)
        self.assertIn(b"Document created !", mailSent)

        api.portal.set_registry_record("plone.email_from_address", email_from_address)
        api.portal.set_registry_record("plone.email_from_name", email_from_name)

    def testExecuteSimpleByAttribute(self):
        self.loginAsPortalOwner()
        self.folder.foo_attr = "member1@dummy.org"
        e = MailFromFieldAction()
        e.source = "foo@bar.be"
        e.fieldName = "foo_attr"
        e.target = "object"
        e.subject = "Subject"
        e.message = "Còntènt '${title}' created in ${url} - Section is '${section_name}' (${section_url}) !"
        ex = getMultiAdapter((self.folder, e, DummyEvent(self.folder.d1)), IExecutable)
        ex()
        mailSent = self.mailhost.messages[0]
        self.assertIn(b'Content-Type: text/plain; charset="utf-8"', mailSent)
        self.assertIn(b"To: member1@dummy.org", mailSent)
        self.assertIn(b"From: foo@bar.be", mailSent)
        self.assertIn(
            b"'D=C3=B2cumento' created in http://nohost/plone/f1/d1 - Sec=\ntion is 'C=C3=A0rtella' (http://nohost/plone/f1) !",
            mailSent,
        )

    def testExecuteTargetByAttribute(self):
        self.loginAsPortalOwner()
        self.folder.d1.foo_attr = "member1@dummy.org"
        e = MailFromFieldAction()
        e.source = "foo@bar.be"
        e.fieldName = "foo_attr"
        e.target = "target"
        e.subject = "Subject"
        e.message = "Còntènt '${title}' created in ${url} - Section is '${section_name}' (${section_url}) !"
        ex = getMultiAdapter((self.folder, e, DummyEvent(self.folder.d1)), IExecutable)
        ex()
        mailSent = self.mailhost.messages[0]
        self.assertIn(b'Content-Type: text/plain; charset="utf-8"', mailSent)
        self.assertIn(b"To: member1@dummy.org", mailSent)
        self.assertIn(b"From: foo@bar.be", mailSent)
        self.assertIn(
            b"'D=C3=B2cumento' created in http://nohost/plone/f1/d1 - Sec=\ntion is 'C=C3=A0rtella' (http://nohost/plone/f1) !",
            mailSent,
        )

    def testExecuteSimpleByMethod(self):
        self.loginAsPortalOwner()
        self.folder.setDescription("member1@dummy.org")
        e = MailFromFieldAction()
        e.source = "foo@bar.be"
        e.fieldName = "Description"
        e.target = "object"
        e.subject = "Subject"
        e.message = "Còntènt '${title}' created in ${url} - Section is '${section_name}' (${section_url}) !"
        ex = getMultiAdapter((self.folder, e, DummyEvent(self.folder.d1)), IExecutable)
        ex()
        mailSent = self.mailhost.messages[0]
        self.assertIn(b'Content-Type: text/plain; charset="utf-8"', mailSent)
        self.assertIn(b"To: member1@dummy.org", mailSent)
        self.assertIn(b"From: foo@bar.be", mailSent)
        self.assertIn(
            b"'D=C3=B2cumento' created in http://nohost/plone/f1/d1 - Sec=\ntion is 'C=C3=A0rtella' (http://nohost/plone/f1) !",
            mailSent,
        )

    def testExecuteTargetByFieldName(self):
        self.loginAsPortalOwner()
        self.folder.d1.text = "member1@dummy.org"
        e = MailFromFieldAction()
        e.source = "foo@bar.be"
        e.fieldName = "text"
        e.target = "target"
        e.subject = "Subject"
        e.message = "Còntènt '${title}' created in ${url} - Section is '${section_name}' (${section_url}) !"
        ex = getMultiAdapter((self.folder, e, DummyEvent(self.folder.d1)), IExecutable)
        ex()
        mailSent = self.mailhost.messages[0]
        self.assertIn(b'Content-Type: text/plain; charset="utf-8"', mailSent)
        self.assertIn(b"To: member1@dummy.org", mailSent)
        self.assertIn(b"From: foo@bar.be", mailSent)
        self.assertIn(
            b"'D=C3=B2cumento' created in http://nohost/plone/f1/d1 - Sec=\ntion is 'C=C3=A0rtella' (http://nohost/plone/f1) !",
            mailSent,
        )

    def testExecuteSimpleByCMFProperty(self):
        self.loginAsPortalOwner()
        self.folder.manage_addProperty("foo_property", "member1@dummy.org", "string")
        e = MailFromFieldAction()
        e.source = "foo@bar.be"
        e.fieldName = "foo_property"
        e.target = "object"
        e.subject = "Subject"
        e.message = "Còntènt '${title}' created in ${url} - Section is '${section_name}' (${section_url}) !"
        ex = getMultiAdapter((self.folder, e, DummyEvent(self.folder.d1)), IExecutable)
        ex()
        mailSent = self.mailhost.messages[0]
        self.assertIn(b'Content-Type: text/plain; charset="utf-8"', mailSent)
        self.assertIn(b"To: member1@dummy.org", mailSent)
        self.assertIn(b"From: foo@bar.be", mailSent)
        self.assertIn(
            b"'D=C3=B2cumento' created in http://nohost/plone/f1/d1 - Sec=\ntion is 'C=C3=A0rtella' (http://nohost/plone/f1) !",
            mailSent,
        )

    def testExecuteFolderModify(self):
        # can happen as rules are not triggered on the rule root itself
        self.loginAsPortalOwner()
        self.folder.foo_property = "member1@dummy.org"
        e = MailFromFieldAction()
        e.source = "foo@bar.be"
        e.fieldName = "foo_property"
        e.target = "object"
        e.subject = "Subject"
        e.message = "Còntènt '${title}' created in ${url} - Section is '${section_name}' (${section_url}) !"
        ex = getMultiAdapter((self.folder, e, DummyEvent(self.folder)), IExecutable)
        ex()
        mailSent = self.mailhost.messages[0]
        self.assertIn(b'Content-Type: text/plain; charset="utf-8"', mailSent)
        self.assertIn(b"To: member1@dummy.org", mailSent)
        self.assertIn(b"From: foo@bar.be", mailSent)
        self.assertIn(
            b"C=C3=A0rtella' created in http://nohost/plone/f1 - Section=\n is 'C=C3=A0rtella' (http://nohost/plone/f1) !",
            mailSent,
        )

    def testExecuteEmptyValue(self):
        self.loginAsPortalOwner()
        self.folder.foo_attr = ""
        e = MailFromFieldAction()
        e.source = "foo@bar.be"
        e.fieldName = "foo_attr"
        e.target = "object"
        e.subject = "Subject"
        e.message = "Còntènt '${title}' created in ${url} - Section is '${section_name}' (${section_url}) !"
        getMultiAdapter((self.folder, e, DummyEvent(self.folder.d1)), IExecutable)()
        self.assertEqual(self.mailhost.messages, [])


def test_suite():
    from unittest import makeSuite, TestSuite

    suite = TestSuite()
    suite.addTest(makeSuite(TestMailAction))
    return suite
