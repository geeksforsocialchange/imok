Feature: Members can check in and out, and an alarm is raised if they don't check out
    In order that I can ensure my personal safety
    As a member
    I want to be able to check in and out
    And have an alarm raised if I don't check out
    And raise the alarm manually if I need to

    Background: I have a registered confirmed account
        Given I have been registered as a member
        And My registration is confirmed
        And email is configured

    Scenario: I can check in
        Given my signing center is "Processing Facility"
        When I send "IN" via twilio at "1919-12-21 20:00:00"
        Then I am checked in
        And the check in time is "1919-12-21 20:00:00"
        And I receive a message containing:
          """
          Your check in time at Processing Facility is 20:00:00.

          I will raise the alarm if you don't check out by 21:00:00.

          I will update your check in time if you message IN again.
          """
        And I am ok

    Scenario: I check out after checking in
        Given my signing center is "Processing Facility"
        When I send "IN" via twilio
        And I send "OUT" via twilio at "1919-12-21 20:30:00"
        Then I am not checked in
        And my check in record is deleted
        And I receive a message containing:
          """
          Your check out time from Processing Facility is 20:30:00.

          I hope you have a lovely day!
          """
        # TODO: Shouldn't this be "ok"?
        And I might be ok

    Scenario: Checking in twice updates the timestamp
        When I send "IN" via twilio at "1983-07-08 20:15:00"
        And I send "IN" via twilio at "1983-07-08 20:20:00"
        Then I am checked in
        And I receive a message containing:
         """
         You were already checked in.

         I updated your check in time to 20:20:00.
         """
        And the check in time is "1983-07-08 20:20:00"
        # TODO: Shouldn't this be "maybe ok"?
        And I am ok

    Scenario: I can't check out without checking in first
        Given I am not checked in
        When I send "OUT" via twilio
        Then I receive a message containing
        """
        You were not checked in.

        To check in, message IN.

        To raise the alarm, message SOS.
        """
        And I am not checked in

    Scenario: When time is nearly up, send a reminder
        Given my signing center is "Government Facility"
        And I am checked in at "1886-05-04 22:00:00"
        And my signing center is "Government Facility"
        When the healthchecker runs at "1886-05-04 22:58:00"
        Then there are 0 overdue checkins
#        @TODO: This would need mocking somewhere
#        And I am sent:
#        """
#        Have you forgotten to sign out? I am about to notify the admins.
#
#        Please send OUT if you have left Government Facility.
#        """
        # TODO: Shouldn't this be "maybe ok"?
        And I am ok
        And there are 1 warning checkins

    Scenario: When time is up, alert the admin team
        Given my signing center is "Government Facility"
        Given I am checked in at "1936-07-17 10:00:00"
        When the healthchecker runs at "1936-07-17 11:00:00"
        Then there are 1 overdue checkins
#        @TODO: This would need mocking somewhere
#        And I am sent:
#        """
#        You didn't check out of Government Facility.
#
#        I notified the admins at 11:00.
#        """
        And I am not ok
        Then an admin is contacted

    Scenario: I manually raise the alarm
        When I send "SOS" via twilio at "2010-05-04 08:10:23"
        Then I receive a message containing:
          """
          Thank you for letting me know.

          I notified the admins at 08:10
          """
        And I am not ok

    Scenario: I send an invalid command
        When I send "Asdasdf" via twilio
        Then I receive a message containing:
        """
        Sorry, I didn't understand that message.

        Send INFO for a list of commands I understand.
        """

    Scenario: I request the server commands again
        Given my signing center is "Government Facility"
        When I send "INFO" via twilio
        Then I receive a message containing:
        """
        Welcome to imok development, Fake User!

        You can send me the following commands, or text +15005550006:

        IN: Check in to Government Facility

        OUT: Check out (after check in)

        NAME: Update your name

        SOS: Raise the alarm

        INFO: Get this message again
        """
        And this message only uses 2 SMS messages to send
