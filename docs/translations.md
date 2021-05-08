# Translations

We welcome additional translations for messages sent to members. Please note we are not currently translating admin messages until reaching a stable version of imok, as this also requires a significant review of Django's available translations. This means that the admin interface is English

You can provide these in your browser using [POEditor](https://poeditor.com/join/project?hash=p2lHT7RFE5).

Fuzzy translations tend to be ignored, so don't mark your translations as fuzzy or incomplete if you are happy with them.

We will periodically add new translations to the project. If this isn't fast enough for you, read on for how to do this yourself.

## New Languages

To integrate additional languages into imok requires a number of steps.  The documentation below describes the steps for Welsh.

1. `django-admin makemessages -l cy_GB` to create the PO files
2. Optionally import this into poeditor to let people provide and edit translations
3. Edit the generated `locale/cy_GB/LC_MESSAGES/django.po` file, either directly or from an export from poeditor
4. Run `django-admin compilemessages` to generate a machine-friendly version
5. Edit `imok/settings.py` to add `('cy-gb', 'Welsh')` to LANGUAGES
6. Edit `application/models.py` to add `('cy_GB', 'Welsh')` to LANGUAGES
7. Run `docker-compose run web python manage.py makemigrations` to list Welsh as an option in the admin screen
8. Run `docker-compose run web python manage.py migrate` to apply the migration created above

You should now be able to select Welsh as an option in the admin panel.

## Editing existing languages

If you need to change or improve the translations then you can do so by following a subset of the above instructions.  These instructions again assume Welsh, change the codes as required.

1. `django-admin makemessages -l cy_GB` to update the PO file with any newly missing strings
2. Optionally import this into poeditor to let people provide the missing translations
3. Edit the generated `locale/cy_GB/LC_MESSAGES/django.po` file, either directly or from an export from poeditor
4. Run `django-admin compilemessages` to generate a machine-friendly version
