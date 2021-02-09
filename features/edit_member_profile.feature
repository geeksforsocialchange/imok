Feature: Members can edit their profile information
  In order that I can keep my information up to date
  As a member
  I want to be able to change my personal information

  Background: I have a registered confirmed account
    Given I have been registered as a member
    And My registration is confirmed

  Scenario: Update my name
    When I send <NAME alice>
    Then My name is <alice>
    And My registration time does not change
