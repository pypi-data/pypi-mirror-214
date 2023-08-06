# -*- coding: utf-8 -*-

try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    # Plone 4.1
    from zope.schema.interfaces import IVocabularyFactory

from collective.contentrules.mailfromfield import messageFactory as _
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


@implementer(IVocabularyFactory)
class TargetElementsVocabulary(object):
    """Vocabulary factory for possible rule target"""

    def __call__(self, context):
        return SimpleVocabulary(
            [
                SimpleTerm("object", "object", _("From rule's container")),
                SimpleTerm(
                    "target",
                    "target",
                    _("From content that triggered the event"),
                ),
                SimpleTerm("parent", "parent", _("From content's parent")),
            ]
        )


targetElements = TargetElementsVocabulary()
