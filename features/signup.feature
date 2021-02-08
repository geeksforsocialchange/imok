Feature: registering a member
  Scenario: register a member
    When I create a new member
    Then The member is not confirmed
    And The member was created recently

  Scenario: confirm registration
    Given I have been registered as a member
    When I reply <Y>
    Then My registration is confirmed
    And My registration time does not change

  Scenario: fix my name
    Given I have been registered as a member
    When I reply <NAME alice>
    Then My name is <alice>
    And My registration time does not change

  Scenario: checkin
    Given I have been registered as a member
    And My registration is confirmed
    When I reply <IN>
    Then I am checked in

#  Scenario: checkin without registration
# @TODO what happens if you try to checkin without being registered?

  Scenario: checkout after checking in
    Given I have been registered as a member
    And My registration is confirmed
    When I reply <IN>
    And I reply <OUT>
    Then I am not checked in

  Scenario: double checkin
    Given I have been registered as a member
    And My registration is confirmed
    When I reply <IN>
    And I reply <IN>
    Then I am checked in
    And I receive a message containing <You were already checked in>

  Scenario: checkout without checkin
    Given I have been registered as a member
    And My registration is confirmed
    And I am not checked in
    When I reply <OUT>
    Then I receive a message containing <You were not signed in>
    And I am not checked in