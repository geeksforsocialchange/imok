Feature: Members can receive messages in their own language
    In order to support members whose first language is not English
    As a project admin
    I want to specify a member's language
    And the member will receive messages in that language

    Background: I have a registered confirmed account
        Given I have been registered as a member who speaks cy-GB
        And My registration is confirmed

    Scenario: I can check in
        When I send "IN" at "1919-12-21 20:00:00"
        Then I am checked in
        And the check in time is "1919-12-21 20:00:00"
        And I receive a message containing "Fe'ch gwiriwyd i mewn yn"
        And I am ok
