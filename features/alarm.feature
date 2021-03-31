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
    When I send "IN" at "1919-12-21 20:00:00"
    Then I am checked in
    And the check in time is "1919-12-21 20:00:00"
    And I receive a message containing "You were checked in at"
    And I am ok

  Scenario: I check out after checking in
    When I send "IN"
    And I send "OUT"
    Then I am not checked in
    And my check in record is deleted
    And I receive a message containing "You were checked out at"
    And I might be ok


  Scenario: Checking in twice updates the timestamp
    When I send "IN" at "1983-07-08 20:15:00"
    And I send "IN" at "1983-07-08 20:20:00"
    Then I am checked in
    And I receive a message containing "You were already checked in. Your check in time has been updated"
    And the check in time is "1983-07-08 20:20:00"
    And I am ok

  Scenario: I can't check out without checking in first
    Given I am not checked in
    When I send "OUT"
    Then I receive a message containing "You were not checked in. To check in message IN"
    And I am not checked in

  Scenario: When time is nearly up, send a reminder
    Given I am checked in at "1886-05-04 22:00:00"
    When the healthchecker runs at "1886-05-04 22:58:00"
    Then there are 0 overdue checkins
    And I am ok
    And there are 1 warning checkins

  Scenario: When time is up, alert the admin team
    Given I am checked in at "1936-07-17 10:00:00"
    When the healthchecker runs at "1936-07-17 11:00:00"
    Then there are 1 overdue checkins
    And I am not ok
    Then an admin is contacted

  Scenario: I manually raise the alarm
    When I send "SOS"
    Then I receive a message containing "Thanks for letting us know, our staff have been notified"
    And I am not ok
