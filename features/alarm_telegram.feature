Feature: Members can check in and out, and an alarm is raised if they don't check out
    In order that I can ensure my personal safety
    As a member
    I want to be able to check in and out
    And have an alarm raised if I don't check out
    And raise the alarm manually if I need to

    Background: I have a registered confirmed account
        Given I have been registered as a member
        And My registration is confirmed
        And I have a telegram chat_id
        And I have a telegram username

    Scenario: I can check in
        When I send "IN" via telegram at "1919-12-21 20:00:00"
        Then I am checked in
        And the check in time is "1919-12-21 20:00:00"
        And I am safe

    Scenario: I check out after checking in
        When I send "IN" via telegram
        And I send "OUT" via telegram
        Then I am not checked in
        And my check in record is deleted
        And I am safe

    Scenario: Checking in twice updates the timestamp
        When I send "IN" via telegram at "1983-07-08 20:15:00"
        And I send "IN" via telegram at "1983-07-08 20:20:00"
        Then I am checked in
        And the check in time is "1983-07-08 20:20:00"
        And I am safe

    Scenario: I can't check out without checking in first
        Given I am not checked in
        When I send "OUT" via telegram
        Then I am not checked in

    Scenario: When time is nearly up, send a reminder
        Given I am checked in at "1886-05-04 22:00:00"
        When the healthchecker runs at "1886-05-04 22:58:00"
        Then there are 0 overdue checkins
        And I am safe
        And there are 1 warning checkins

    Scenario: When time is up, alert the admin team
        Given I am checked in at "1936-07-17 10:00:00"
        When the healthchecker runs at "1936-07-17 11:00:00"
        Then there are 1 overdue checkins
        And I am not safe
        Then an admin is contacted

    Scenario: I manually raise the alarm
        When I send "SOS" via telegram
        Then I am not safe


    Scenario Outline: Telegram usernames are validated
        When I validate telegram username <username>
        Then I see the error <return>

        Examples:
        | username | return |
        | bob      | <class 'django.core.exceptions.ValidationError'> |
        | @bob     | <class 'django.core.exceptions.ValidationError'> |
        | alice    | None            |
        | @alice   | <class 'django.core.exceptions.ValidationError'> |
        | f45c54dd41cf3c1ebb3ec935b943a104  | None |
        | f45c54dd41cf3c1ebb3ec935b943a104a | <class 'django.core.exceptions.ValidationError'> |
        | @f45c54dd41cf3c1ebb3ec935b943a104 | <class 'django.core.exceptions.ValidationError'> |

    Scenario: Duplicate telegram usernames are not allowed
        When I create a member with a duplicate telegram username
        Then I see the error <class 'django.db.utils.IntegrityError'>
