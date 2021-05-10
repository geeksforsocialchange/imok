import os

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
    context.test.assertIn((lower_dashed_locale(locale), language), settings.LANGUAGES)


@then(u'the language {language} maps to {locale} in the members model')
def step_impl(context, language, locale):
    from application import models
    context.test.assertIn((locale, language), models.LANGUAGES)


@then(u'the locale {locale} can be activated')
def step_impl(context, locale):
    translation.activate(locale)


@then(u'the {locale} mo file is newer than the po file')
def step_impl(context, locale):
    po_file = Path(os.path.join(settings.BASE_DIR, "locale", locale, "LC_MESSAGES", "django.po"))
    mo_file = Path(os.path.join(settings.BASE_DIR, "locale", locale, "LC_MESSAGES", "django.mo"))
    context.test.assertTrue(mo_file.stat().st_mtime >= po_file.stat().st_mtime)


@given(u'the reference locale {locale}')
def step_impl(context, locale):
    po_file = Path(os.path.join(settings.BASE_DIR, "locale", locale, "LC_MESSAGES", "django.po"))
    context.reference_po = polib.pofile(po_file)
    mo_file = Path(os.path.join(settings.BASE_DIR, "locale", locale, "LC_MESSAGES", "django.mo"))
    context.reference_mo = polib.mofile(mo_file)

    context.test.assertEqual(len(context.reference_po), len(context.reference_mo))


@then(u'the other language files should be the same length')
def step_impl(context):
    for po_file in glob.glob(os.path.join(settings.BASE_DIR, 'locale', '*_*', 'LC_MESSAGES', 'django.po')):
        context.test.assertEqual(len(polib.pofile(po_file)), len(context.reference_po))
    for mo_file in glob.glob(os.path.join(settings.BASE_DIR, 'locale', '*_*', 'LC_MESSAGES', 'django.mo')):
        context.test.assertEqual(len(polib.mofile(mo_file)), len(context.reference_mo))


def lower_dashed_locale(locale):
    return locale.lower().replace('_', '-')
