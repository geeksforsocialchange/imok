# Use Django's authentication for user management

* Status: proposed
* Deciders: Kim, Alice
* Date: 2020-02-01

## Context and Problem Statement

We need to ensure the site is highly secure against fascists and trolls, but we also need the website to be simple for admin users.

## Decision Drivers

* Limited budget
* Desire to not use Amazon services
* Need to run on multiple devices (including iPad)
* Needs to be secure
* Rather not rely on an external email provider

## Considered Options

* Auth0 (including paid and free options, and including their various offerings)
* Django's in-built user management

## Decision Outcome

Chosen option: "Django's in-built user management", because it comes for free and meets the requirements.

### Positive Consequences

* Limited additional work to secure it
* No additional third-parties to deal with

### Negative Consequences

* We need to be confident we are managing passwords securely
* More work to enforce 2FA if we need this

## Pros and Cons of the Options <!-- optional -->

### Auth0

Auth0 provides a number of methods for managing users.  This simplest being a database of users, which can be used with a Django plugin.  The most complicated being passwordless, which would require custom code.

* Good, because we don't store passwords ourselves
* Good, because it can provide 2FA (if you pay or integrate with Twilio)
* Bad, because we are expected to maintain email services
* Bad, because the free version is not considered production-ready
* Bad, because the user-flow isn't clean
* Bad, because it requires a Django plugin
* Bad, because we have to maintain the Auth0 integration
* Bad, because it is a third-party we have to deal with

### [option 2]

Django comes with user management out of the box.

* Good, because no third-parties
* Good, because it integrates with the inbuilt admin dashboard easily
* Bad, because we need to maintain email services
* Bad, because 2FA isn't as easy to add