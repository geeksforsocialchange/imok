# Translations

We welcome additional translations for messages sent to members. Please note we are not currently translating admin messages until reaching a stable version of imok, as this also requires a significant review of Django's available translations. This means that the admin interface is in English only at present.

**[You can submit translations directly in your browser using POEditor](https://poeditor.com/join/project?hash=p2lHT7RFE5).**

Fuzzy translations tend to be ignored, so don't mark your translations as fuzzy or incomplete if you are happy with them.

We will periodically add new translations to the project. If this isn't fast enough for you, read on for how to do this yourself.

## How to add new translations

Adding additional languages requires a number of steps. If you are unable to follow these steps then feel free to raise a GitHub issue requesting the new language, or join our [Discord server](https://discord.gg/4JKak6aymM). The documentation below describes how you would add a Welsh translation as an example.

1. `django-admin makemessages -l cy_GB --ignore venv` to create the PO file
1. Add the language to POEditor if you have access
1. If you can provide translations, do so by either editing the generated `locale/cy_GB/LC_MESSAGES/django.po` file directly or by copying across the exported PO file from POEditor
1. Run `docker-compose run web python manage.py compilemessages` to compile the translation file
1. Edit `imok/settings.py` to add `('cy-gb', 'Welsh')` to LANGUAGES
1. Edit `application/models.py` to add `('cy_GB', 'Welsh')` to LANGUAGES
1. Run `docker-compose run web python manage.py makemigrations` to list Welsh as an option in the admin screen
1. Run `docker-compose run web python manage.py migrate` to apply the migration created above
1. Raise a pull request for this new language, and request it be added to POEditor if it hasn't already

You should now be able to select Welsh as an option in the admin panel.

## How to improve existing translations

You can provide improved translations through [POEditor](https://poeditor.com/join/project?hash=p2lHT7RFE5) and then either raise a GitHub issue requesting it be imported or raise a pull request yourself:

1. Submit the changes via POEditor
1. Export the language as a PO file
1. Copy this PO file over the top of the appropriate file in the repository
1. Run `docker-compose run web python manage.py compilemessages` to compile the translation file
1. Raise a pull request

## How to update the reference translation when imok is updated

When new strings are added or edited to the base project, the base (English) translation file needs to be updates.

1. `django-admin makemessages -l en_GB --ignore venv --no-obsolete` to update the reference translation.
1. Import the generated `locale/en_GB/LC_MESSAGES/django.po` file into POEditor
1. Update the English translation in POEditor and export back to `locale/en_GB/LC_MESSAGES/django.po`
1. Run `docker-compose run web python manage.py compilemessages` to compile the translation file
1. Raise a pull request with this new string, and (optionally) notify translators that there are new strings to translate
