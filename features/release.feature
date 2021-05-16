Feature: Generate deployment notes
    As an administrator
    I want to know when the server is updated
    So that I can be aware of unexpected side effects

#    It's hard to test the sending of Telegram messages, but we can test the contents of the message
    Scenario Outline:
        Given git rev <rev>
        Then the deployment message contains <string>
        Examples:
            | rev                                      | string                             |
            | 4e9593f19345a7feec452a33a636a0b9b7a16a6a | Release: 0.1.0                     |
            | 31fe54b4638e1f2fc45263aad90f999b0c9ef6aa | Init                               |
            | abc123                                   | This commit was not found upstream |
