import os
import re

from behave import given, when, then
from django.conf import settings
from django.utils import translation
import polib
import glob

from pathlib import Path


@given(u'I want to use the language {language}')
def step_impl(context, language):
    pass


@then(u'the {locale} directory exists')
def step_impl(context, locale):
    directory = Path(os.path.join(settings.BASE_DIR, "locale", locale, "LC_MESSAGES"))
    print(directory)
    context.test.assertTrue(directory.is_dir())


@then(u'the {locale} po file is valid')
def step_impl(context, locale):
    file = Path(os.path.join(settings.BASE_DIR, "locale", locale, "LC_MESSAGES", "django.po"))
    polib.pofile(file)
    context.test.assertTrue(file.is_file())


@then(u'the {locale} mo file is valid')
def step_impl(context, locale):
    file = Path(os.path.join(settings.BASE_DIR, "locale", locale, "LC_MESSAGES", "django.mo"))
    polib.mofile(file)
    context.test.assertTrue(file.is_file())


@then(u'the language {language} maps to {locale} in settings.py')
def step_impl(context, language, locale):
    context.test.assertIn((translation.to_language(locale), language), settings.LANGUAGES)


@then(u'the language {language} maps to {locale} in the members model')
def step_impl(context, language, locale):
    from application import models
    context.test.assertIn((locale, language), models.LANGUAGES)


@then(u'the locale {locale} can be activated')
def step_impl(context, locale):
    translation.activate(locale)


@given(u'the reference locale {locale}')
def step_impl(context, locale):
    po_file = Path(os.path.join(settings.BASE_DIR, "locale", locale, "LC_MESSAGES", "django.po"))
    context.reference_po = polib.pofile(po_file)
    mo_file = Path(os.path.join(settings.BASE_DIR, "locale", locale, "LC_MESSAGES", "django.mo"))
    context.reference_mo = polib.mofile(mo_file)

    context.test.assertEqual(len(context.reference_po), len(context.reference_mo))


@then(u'the locale {locale} is not missing any tokens')
def step_impl(context, locale):
    po_file = Path(os.path.join(settings.BASE_DIR, "locale", locale, "LC_MESSAGES", "django.po"))
    po = polib.pofile(po_file)
    for string in po:
        if len(string.msgstr) == 0:
            continue
        print(len(string.msgstr))
        print(len(string.msgid))
        regexp = re.compile(r'(%\(.+?\)[a-z])')
        source_tokens = re.findall(regexp, string.msgid)
        translation_tokens = re.findall(regexp, string.msgstr)

        # Assert that each token in the source can also be found in the translation
        for t in source_tokens:
            context.test.assertIn(t, string.msgstr)

        # Assert that each token in the translation can also be found in the source
        for t in translation_tokens:
            context.test.assertIn(t, string.msgid)

        # Assert that the number of tokens in the source and translation are the same
        context.test.assertEqual(len(source_tokens), len(translation_tokens))
