from django.test import TestCase
from .models import Member, Checkin
from django.test import Client
from django.utils import timezone
from django.db import transaction


def time_within(timestamp, timedelta):
    now = timezone.now()
    return now - timedelta < timestamp < now + timedelta


def cleardown_checkins(phone_number='+12025550483'):
    member = Member.objects.get(phone_number=phone_number)
    try:
        Checkin.objects.get(member=member).delete()
    except Checkin.DoesNotExist:
        pass


class MemberTests(TestCase):
    def setUp(self):
        member = Member(phone_number='+12025550483', name="Fake User")
        member.save()
        self.assertFalse(member.registered)
        self.assertTrue(time_within(member.registered_at, timezone.timedelta(seconds=10)))
        self.registered_at = member.registered_at

    def test_fix_name(self):
        c = Client()
        response = c.post('/application/twilio', {'From': '+12025550483', 'Body': 'NAME alice'})
        self.assertEqual(response.status_code, 200)
        content = str(response.content, 'utf-8')
        self.assertIn('alice', content)

        member = Member.objects.get(phone_number='+12025550483')
        self.assertEqual(member.name, 'alice')

        # Assert that saving doesn't change the time the member was registered:
        self.assertEqual(member.registered_at, self.registered_at)

    def test_confirm_account(self):
        c = Client()
        response = c.post('/application/twilio', {'From': '+12025550483', 'Body': 'YES'})
        self.assertEqual(response.status_code, 200)

        member = Member.objects.get(phone_number='+12025550483')
        self.assertTrue(member.registered)

        # Assert that confirming an account doesn't change the time the member was registered:
        self.assertEqual(member.registered_at, self.registered_at)

    def test_checkin(self):
        cleardown_checkins()

        c = Client()
        response = c.post('/application/twilio', {'From': '+12025550483', 'Body': 'IN'})
        self.assertEqual(response.status_code, 200)

        member = Member.objects.get(phone_number='+12025550483')
        checkin = Checkin.objects.get(member=member)
        self.assertTrue(time_within(checkin.time_stamp, timezone.timedelta(seconds=10)))

    def test_double_checkin(self):
        cleardown_checkins()
        c = Client()
        with transaction.atomic():
            c.post('/application/twilio', {'From': '+12025550483', 'Body': 'IN'})
        with transaction.atomic():
            response = c.post('/application/twilio', {'From': '+12025550483', 'Body': 'IN'})
        self.assertEqual(response.status_code, 200)
        content = str(response.content, 'utf-8')
        self.assertIn('You were already checked in', content)

        member = Member.objects.get(phone_number='+12025550483')
        self.assertEqual(Checkin.objects.filter(member=member).count(), 1)

    def test_checkout(self):
        """
        check in and then check out
        """
        cleardown_checkins()
        c = Client()
        with transaction.atomic():
            c.post('/application/twilio', {'From': '+12025550483', 'Body': 'IN'})
        with transaction.atomic():
            response = c.post('/application/twilio', {'From': '+12025550483', 'Body': 'OUT'})
        self.assertEqual(response.status_code, 200)
        content = str(response.content, 'utf-8')
        self.assertIn('You signed out of', content)

        member = Member.objects.get(phone_number='+12025550483')
        self.assertEqual(Checkin.objects.filter(member=member).count(), 0)

    def test_checkout_when_not_checked_in(self):
        """
        clear down checkins, then try to check out
        """
        cleardown_checkins()
        c = Client()
        response = c.post('/application/twilio', {'From': '+12025550483', 'Body': 'OUT'})
        self.assertEqual(response.status_code, 200)
        content = str(response.content, 'utf-8')
        self.assertIn('You were not signed in', content)
