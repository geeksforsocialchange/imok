Feature: An admin telegram group gets updated when there is an alert
    In order that we can support people who don't sign out
    As a signing support network administrator
    I want to get notifications when bad things happen

    Scenario Outline: Someone didn't sign out
        Given Mo Member has notes <notes>
        And Mo Member has a signing center of "Government Facility"
        And Mo Member has a phone number of "+447740000000"
        And Mo Member signed in at "1936-07-17 09:00:00"
        And Mo Member didn't sign out at "1936-07-17 10:00:00"
        When the healthchecker runs at "1936-07-17 11:00:00"
        Then there are 1 overdue checkins
        And the admins receive a message containing:
        """
        ⚠️ Mo Member (+447740000000) didn't sign out of Government Facility.

        ⏰ They signed in at 09:00 on 17/07/1936.
        """
        And the admins receive a message containing <output>
        Examples:
        | notes | output |
        | None  | There are no notes saved for this member |
        | My emergency contact is Mum Member on +447740000000 | My emergency contact is Mum Member on +447740000000 |



    Scenario Outline: Someone raised the alarm
        Given Mo Member has notes <notes>
        And Mo Member has a phone number of "+447740000000"
        And Mo Member has a signing center of "Government Facility"
        And Mo Member raises the alarm at "2020-10-01 23:12:12"
        Then the admins receive a message containing:
        """
        ⚠️ Mo Member (+447740000000) sent an SOS at Government Facility.

        ⏰ They raised it at 23:12 on 01/10/2020.
        """
        And the admins receive a message containing <output>
        Examples:
        | notes | output |
        | None  | There are no notes saved for this member |
        | My emergency contact is Mum Member on +447740000000 | My emergency contact is Mum Member on +447740000000 |
