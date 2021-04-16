# I'm OK (imok)

Imok is a simple bot that lets you check in by a text or DM before doing potentially risky activities. If you don't check in again saying you're ok after a pre-chosen time (say 30 minutes), it will raise the alarm with a third party.

Examples use cases are:

- Going to a protest where you might be arrested
- Women and gender minorities walking home at night, or going on dates
- Asylum seekers who have to check in to state processing facilities where they might be detained

We do not currently offer a public instance of imok so it is currently aimed mostly at local mutual aid and support groups with the capacity to set up a version for their local community.

Imok was initially developed for the latter use case of and is a collaboration between [No Borders Manchester](https://nobordersmcr.com/), [Resistance Lab](https://resistancelab.network) and [Geeks for Social Change](https://gfsc.studio).

We currently support SMS and Telegram. We are looking to support WhatsApp and Signal soon.

## Installation

Setting up imok currently requires a little bit of technical know-how. You'll need to be comfortable setting up a virtual server (we use Digital Ocean), running some commands in the terminal, and generally have some confidence deploying web applications. You'll also need to register for a Twilio account and set up an API key. We hope to make this easier in the future.

Imok is potentially expensive to run due to the cost of SMS messages which cost about 4p at the time of writing. With a few dozen users using it multiple times per day this can quickly add up. If your intended users are able to access this entirely through Telegram the cost is nearly zero.

See [installation.md](docs/installation.md) for more information.

We can also set up an installation for you for a fee. All funds raised go towards improving imok. Email [kim@gfsc.studio](mailto:kim@gfsc.studio) if you'd like to chat about this.

## How it works (admins)

Imok currently works on an 'allowlist' basis, where you will identify individuals through real-life interactions and then add them to your imok server. This cuts down on your costs and keeps the installation more secure.

1. You add people you want to support in the imok admin interface ('members')
1. imok will send an SMS inviting the person to register
1. You can then see who is currently signed in using the imok admin interface
1. If the alarm is tripped, administrators receive an email

We will be further developing admin documentation as the project develops.

We are planning to allow public instances that anyone can register on at a later date.

## How it works (member)

As a member of an imok instance:

1. You will receive a text asking if you want to join the server
1. You can then text the number `IN` to register that you may be in danger
1. If you text `OUT` within the designated time period, nothing happens
1. If you don't, the administrator is notified and can begin to find out what happened

That's it! There are a few more commands that we will be listing on the project wiki in due course.

## Contributing

We welcome contributors to help with this project. Imok is written in Django.

See [development.md](docs/development.md) for how to set up a development environment.

## Donations

Imok has been developed entirely by volunteers. If you'd like to support imok and more software like it, please consider sending us a one-off or regular donation.

<script type='text/javascript' src='https://storage.ko-fi.com/cdn/widget/Widget_2.js'></script><script type='text/javascript'>kofiwidget2.init('Support imok on ko-fi', '#29abe0', 'M4M43THUM');kofiwidget2.draw();</script>
