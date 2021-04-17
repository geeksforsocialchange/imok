Feature: Main admin can control who has access to the admin interface
    In order that I can manage my team and keep data secure
    As a signing support network administrator
    I want to control who has access

    Background: I am an administrator
        Given I have been registered as a superuser

    Scenario: Create read-only user
        When I create a read-only user
        Then the user has permissions to view members
        But the user does not have permission to edit members

    Scenario: Create admin user
        When I create an admin user
        Then the user has permissions to view members
        And the user has permission to edit members
