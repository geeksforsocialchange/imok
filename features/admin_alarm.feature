Feature: An admin telegram group gets updated when there is an alert
    In order that we can support people who don't sign out
    As a signing support network administrator
    I want to get notifications when bad things happen

    Scenario: Someone didn't sign out
        Given Mo Member signed in at "1936-07-17 09:00:00"
        And Mo Member didn't sign out at "1936-07-17 10:00:00"
        When the healthchecker runs at "1936-07-17 11:00:00"
        Then there are 1 overdue checkins
        And the admins recieve a message containing:
        """
        Mo Member (07740000000) didn't sign out of Government Facility.

        They signed in at 09:00 on 17/07/1936.
        """
        And if they have no notes I recieve a message containing "There are no notes saved for this member"
        And if they have notes I recieve a message containing "Notes: My emergency contact is Mum Member on 07740000000"

    Scenario: Someome raised the alarm
        Given Mo Member raises the alarm at "2020-10-01 23:12:12"
        Then the admins recieve a message containing:
        """
        Mo Member (07740000000) sent an SOS at Government Facility.

        They raised it at 23:12 on 01:10:2020.
        """
        And if they have no notes I recieve a message containing "There are no notes saved for this member"
        And if they have notes I recieve a message containing "Notes: My emergency contact is Mum Member on 07740000000"
