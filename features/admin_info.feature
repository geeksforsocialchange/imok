Feature: Admins can see information about members

    Background: I am an administrator
        Given I have been registered as a staff user

    Scenario Outline:
        Given I have permission to view <object>
        When I login
        Then I can see <object>
        Examples:
            | object     |
            | member     |
            | checkin    |
            | metrichour |

    Scenario Outline:
        Given I do not have permission to view <object>
        When I login
        Then I can not see <object>
        Examples:
            | object     |
            | member     |
            | checkin    |
            | metrichour |
