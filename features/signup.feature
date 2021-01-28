Feature: registering for the service after an admin has made me an account
  In order that someone can be notified if I don't check in
  As an asylum seeker
  I want to submit enough information so that someone can raise the alarm

  Scenario: register my name
     Given I recieve a message asking for my name
      When I reply with my name
      Then I recieve a confirmation that my name has been registered
       And I recieve a message asking for my emergency contact details

  Scenario: register my emergency contact details
     Given I recieve a message asking for my emergency contact details
      When I reply with an email address or phone number
      Then I recieve a confirmation that it has been saved
