Feature: Public pages
    In order that there is some kind of hint imok exists
    As a project admin
    I want to see some information on the root url

    Scenario: The root url welcomes me if there are no members
      When there are no members
      And I request '/'
      Then I see 'Welcome to imok'

      Scenario: The root url is quiet if there are one or more members
        When there are members
        And I request '/'
        Then I do not see 'Welcome to imok'
