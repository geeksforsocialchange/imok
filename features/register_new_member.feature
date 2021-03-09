Feature: Admins can register new members
  In order that I can ensure members have been properly registered
  As a project admin
  I want to register a new member on imok
  And have confirmation when they are successfully registered

  Scenario: Admin sends an invitation to member
    Given Admin Angela has logged in with an admin account
    When Admin Angela creates a new member
    Then the member is not confirmed
    And the member was created recently

  Scenario: Member confirms registration
    Given Mo Member has been registered as a member
    And has received a message containing <Welcome to imok!>
    When Mo Member replies <Y>
    Then Mo Member's registration is confirmed
    And Mo Member's registration time does not change

  Scenario: Admin can see that member is registered
    Given Admin Angela has logged in with an admin account
    And Mo Member's registration is confirmed
    Then Admin Angela can see that Mo Member's account registration was confirmed

  Scenario: Unknown Umberto tries to register
    Given An unknown number messages the imok number <Y>
    Then No response is sent
    And the admins are emailed
