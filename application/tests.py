from django.test import TestCase
from .models import Member


# Create your tests here.
class UserTests(TestCase):
    def test_create_member(self):
        user = Member(phone_number='+1202-555-0483', name='Fake User')
        user.save()
