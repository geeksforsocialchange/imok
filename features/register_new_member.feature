Feature: Admins can register new members
  In order that I can ensure members have been properly registered
  As a project admin
  I want to register a new member on imok
  And have confirmation when they are successfully registered

  Background: Email is configured
      Given email is configured

  Scenario: Admin sends an invitation to member
      Given Admin Angela has logged in with an admin account
      When Admin Angela creates a new member
      Then the member is not confirmed
      And the member was created recently

  @twilio
  Scenario: Member confirms registration
      Given Mo Member has been registered as a member
      And Mo Member has been welcomed with:
      """
      You've been invited to join imok development!

      Would you like to register for this service?

      Reply YES to join.
      """
      And Mo Member's signing center is Government Facility
      When Mo Member replies <YES> at "1999-10-10 05:10:10"
      Then Mo Member's registration is confirmed
      And Mo Member's registration time does not change
      And Mo Member receives a message containing:
      """
      Welcome to imok development, Mo Member!

      You can send me the following commands, or text +15005550006:

      IN: Check in to Government Facility

      OUT: Check out (after check in)

      NAME: Update your name

      SOS: Raise the alarm

      INFO: Get this message again

      You can also message me on Telegram: Telegram not configured!
      """
      And this message only uses 2 SMS messages to send
      Then Admin Angela receives a message in a Telegram group containing: "🎉 Mo Member (+447740000000) successfully activated their account at 05:10:10 on 10/10/99!"

  Scenario: Admin can see that member is registered
      Given Admin Angela has logged in with an admin account
      And Mo Member's registration is confirmed
      Then Admin Angela can see that Mo Member's account registration was confirmed

  Scenario: Unknown Umberto tries to register
      Given An unknown number messages the imok number <Y>
      Then No response is sent
      And the admins are emailed
