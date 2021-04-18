Feature: Metrics on number of checkins are tracked
    In order that I can keep track of busy periods
    As a project admin
    I want a count of checkins by hour and signing center

    Background: There are members
        Given Mo Member has been registered as a member
        And has received a message containing <Welcome to imok!>

    Scenario: Single checkin
        When Mo Member replies <IN>
        Then There is 1 checkin

    Scenario: Two checkins
        When Mo Member replies <IN>
        And Mo Member replies <IN>
        Then There are 2 checkins
