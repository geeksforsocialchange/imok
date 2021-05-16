import os

from django.core.management.base import BaseCommand
from application.contact_admins import notify_admins
import requests


def commit_message(rev):
    r = requests.get(f"https://api.github.com/repos/geeksforsocialchange/imok/git/commits/{rev}")
    if r.status_code == 404:
        return "This commit was not found upstream"
    else:
        notes = f"Commit: {rev}\n" \
               f"Committer: {r.json()['committer']['name']}\n" \
               f"Message: {r.json()['message']}\n"\
               f"URL: {r.json()['html_url']}"
        tags = requests.get("https://api.github.com/repos/geeksforsocialchange/imok/tags")
        releases = list(filter(lambda x: x['commit']['sha'] == rev, tags.json()))
        if len(releases) == 1:
            notes = f"{notes}\n" \
                    f"Release: {releases[0]['name']}"
        return notes


def release():
    git_rev = os.getenv("GIT_REV")
    notify_admins("New deployment", f"A new version of imok was deployed\n{commit_message(git_rev)}")


class Command(BaseCommand):
    def handle(self, **options):
        print(release())
