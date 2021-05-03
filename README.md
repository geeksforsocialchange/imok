# I'm OK (imok)

Imok is a simple bot to support people undertaking potentially risky activities. It's aimed at community groups who support these vulnerable people.

The bot lets users 'check in' to the service with a messaging app or SMS message. If users don't 'check out' after 30 minutes (for example), it will raise an alarm in a Telegram groupchat.

Example use cases are:

- Supporting protestors at risk of arrest or kidnapping
- Supporting women and gender minorities walking home at night, or going on dates
- Supporting asylum seekers through 'signing in' processes (see #AbolishReporting on Twitter).

Imok is currently optimised for the latter use case. It is a collaboration between [No Borders Manchester](https://nobordersmcr.com/) and [Geeks for Social Change](https://gfsc.studio) that emerged from the [Resistance Lab](https://resistancelab.network) collective.

We do not currently offer a public instance of imok, and so you will need to set up your own server to use it. The target audience is therefore local mutual aid and community support groups with the capacity and confidence to run a web service.

We currently support SMS, Telegram and WhatsApp. We are looking to support other services too.

## Installation

Setting up imok currently requires a little bit of technical know-how. You'll need to be comfortable setting up a VPS, running terminal commands, and deploying web applications. To support SMS you'll also need to register for a Twilio account and set up an API key.

By default imok uses Telegram as it is secure and free to send messages on. For a real world installation you will want to set up SMS using Twilio. However, this can get expensive: SMS messages cost about $0.04 at the time of writing. With a few dozen users using it several times per day this can quickly add up. If your intended users are able to access this entirely through Telegram the cost is nearly zero.

See [installation.md](docs/installation.md) for more information.

We can also set up an installation for you for a fee. All funds raised go towards improving imok. Email [kim@gfsc.studio](mailto:kim@gfsc.studio) if you'd like to chat about this.

## How it works (admins)

Imok currently requires an admin to invite new users to the system. We expect these invites to happen in community venues and at protests for example. This is both for server security and to keep costs down.

1. You add people you want to support in the imok admin interface ('members')
1. imok will send an SMS inviting the person to register
1. If a timer expires or a member sends an SOS message, it sends a notification to the admin groupchat

We will be further developing admin documentation as the project develops.

## How it works (member)

As a member of an imok instance:

1. You will receive an SMS asking if you want to join the server. After replying to this, the system registers you.
1. You can then text the number `IN` before conducting the risky activity
1. If you text `OUT` within the designated time, nothing happens
1. If you don't, admins get notified that something is wrong
1. If you text `SOS`, admins are immediately notified

That's it! There are a few more commands that we will be listing on the project wiki in due course.

## Contributing

### Software development

We welcome contributors to help with this project. Imok is written in Django.

See [development.md](docs/development.md) for how to set up a development environment.

### Translations

Imok allows language selection for users. Currently available translations are in the [locales](locales) directory. We welcome translation into other languages.

Please note server commands in caps ('YES', 'IN', 'OUT' etc.) are not currently translatable. Please leave these in English in your translations.

[Sign up on POEditor](https://poeditor.com/projects/view?id=428751) to submit a translation.

Translations will be periodically reviewed and added to the project. If you'd like to add translations yourself see [translation.md](docs/translation.md).

## Donations

Imok has been developed entirely by volunteers. If you'd like to support development, please consider sending us a one-off or regular donation.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/M4M43THUM)

## License

Imok is released under the [MIT license](LICENSE).
