Feature: Members can receive messages in their own language
    In order to support members whose first language is not English
    As a project admin
    I want to specify a member's language
    And the member will receive messages in that language

    Scenario Outline:
        Given I have been registered as a member who speaks <language>
        When I send "IN"
        Then I receive a message containing "<reply>"

        Examples:
            | language | reply                    |
            | cy-gb    | Fe'ch gwiriwyd i mewn yn |

    Scenario Outline:
        Given I have been registered as a member who speaks <language>
        When I send "OUT"
        Then I receive a message containing "<reply>"
        Examples:
            | language | reply                          |
            | cy-gb    | Ni chawsoch eich gwirio i mewn |

    Scenario Outline:
        Given I have been registered as a member who speaks <language>
        When I send "IN"
        And I send "OUT"
        Then I receive a message containing "<reply>"
        Examples:
            | language | reply                          |
            | cy-gb    | Fe'ch gwiriwyd ar dallas court |

    Scenario Outline:
        Given I have been registered as a member who speaks <language>
        When I send the command <command>
        Then it returns <response>
        Examples:
            | language | command | response                         |
            | cy-gb    | sos     | Diolch am roi gwybod i ni        |
            | cy-gb    | name    | Rydych chi wedi gosod eich enw i |
            | cy-gb    | yes     | Diolch am gofrestru              |
            | en-gb    | sos     | Thanks for letting us know       |
            | en-gb    | name    | You have set your name to        |
            | en-gb    | yes     | Thanks for registering           |
