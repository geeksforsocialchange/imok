from django.test import TestCase
from .models import Subscriber


# Create your tests here.
class UserTests(TestCase):
    def test_create_user(self):
        user = Subscriber(phone_number='+1202-555-0483', name='Fake User')
        user.save()
