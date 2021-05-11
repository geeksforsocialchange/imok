Feature: translation support
    In order to support members in multiple languages
    As a developer
    I want to know that locales are configured correctly

    Scenario Outline: Supported locales are working
        Given I want to use the language <language>
        Then the <locale> directory exists
        And the <locale> po file is valid
        And the <locale> mo file is valid
        And the language <language> maps to <locale> in settings.py
        And the language <language> maps to <locale> in the members model
        And the locale <locale> can be activated
        And the locale <locale> is not missing any tokens

        Examples:
        | language | locale |
        | English  | en_GB  |
        | French   | fr_FR  |
        | German   | de_DE  |
        | Arabic   | ar     |

    Scenario: locale files are the same length
        Given the reference locale en_GB
        Then the other language files should be the same length
