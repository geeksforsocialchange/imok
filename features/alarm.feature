Feature: Members can check in and out, and an alarm is raised if they don't check out
  In order that I can ensure my personal safety
  As a member
  I want to be able to check in and out
  And have an alarm raised if I don't check out
  And raise the alarm manually if I need to

  Background: I have a registered confirmed account
    Given I have been registered as a member
    And My registration is confirmed

  Scenario: I can check in
    When I send "IN"
    Then I am checked in
    And the check in time is now
    And I recieve a message containing "You were checked in at"

  Scenario: I check out after checking in
    When I send "IN"
    And I send "OUT"
    Then I am not checked in
    And my check in record is deleted
    And I recieve a message containing "You were checked out at"

  Scenario: Checking in twice updates the timestamp
    When I send "IN"
    And I send "IN" again
    Then I am checked in
    And I receive a message containing "You were already checked in. Your check in time has been updated"
    And my check in time is updated

  Scenario: I can't check out without checking in first
    When I am not checked in
    And I send "OUT"
    Then I receive a message containing "You were not checked in. To check in message IN"
    And I am not checked in

  Scenario: When time is nearly up, send a reminder
    When I am checked in
    And the alert time is nearly up
    Then I recieve a message containing "Are you OK? The alarm will be raised in 2 minutes. Text OUT if you’re OK."

  Scenario: When time is up, alert the admin team
    When I am checked in
    And the alert time is exceeded
    Then I recieve a message containing "We will now raise the alarm"
    And an admin is contacted

  Scenario: I manually raise the alarm
    When I send "SOS"
    I recieve a message containing "Thanks for letting us know, our staff have been notified"
    And an admin is contacted
