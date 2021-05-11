# I'm OK (imok)

Imok is a simple bot to support people undertaking potentially risky activities. It's aimed at community groups who support these vulnerable people.

The bot lets users 'check in' to the service with an SMS or messaging app. If users don't 'check out' after 30 minutes (for example), it will raise an alarm in a Telegram groupchat.

Example use cases are:

- Supporting protestors at risk of arrest or kidnapping
- Supporting women and gender minorities walking home at night, or going on dates
- Supporting journalists or medical staff in warzones
- Supporting asylum seekers through 'signing in' processes (see #AbolishReporting on Twitter).

Imok is currently optimised for the latter use case. It is a collaboration between [No Borders Manchester](https://nobordersmcr.com/) and [Geeks for Social Change](https://gfsc.studio) that emerged from the [Resistance Lab](https://resistancelab.network) collective.

We do not currently offer a public instance of imok, and so you will need to set up your own server to use it. The target audience is therefore local mutual aid and community support groups with the capacity and confidence to run a web service.

We currently support SMS and Telegram. WhatsApp is theoretically supported but requires a [WhatsApp Business API account](https://www.whatsapp.com/business/api/?lang=en), which we do not have.

## How it works

### For support workers (admins)

Imok currently requires an admin to invite new users to the system. We expect these invites to happen in community venues and at protests for example. This is both for server security and to keep costs down.

1. You add people you want to support ('members') in the imok admin interface
1. imok will send an SMS inviting the person to register
1. Once the person responds to the SMS to confirm they wish to register, the admin groupchat is notified
1. If a timer expires or a member sends an SOS message, it sends a notification to the admin groupchat

We will be further developing admin documentation as the project develops.

### For members

As a member of an imok instance:

1. You will receive an SMS asking if you want to join the server. After replying to this, the system registers you.
1. You can then text the number `IN` before conducting the risky activity
1. If you text `OUT` within the designated time, nothing happens
1. If you don't, admins get notified that something is wrong
1. If you text `SOS`, admins are immediately notified

That's it! There are a few more commands that we will be listing on the project wiki in due course.

## Deployment

Getting this up and running in the real world requires at least one person comfortable with setting up a server, and a few people to actually run the service on the ground.

### Setting up a server

Setting up imok currently requires a little bit of technical know-how. You'll need to be comfortable setting up a VPS, running terminal commands, and deploying web applications. To support SMS you'll also need to register for a Twilio account and set up an API key.

By default imok uses Telegram as it is secure and free to send messages on. For a real world installation you will want to set up SMS using Twilio. However, this can get expensive: SMS messages cost about $0.04 at the time of writing. With a few dozen users using it several times per day this can quickly add up. If your intended users are able to access this entirely through Telegram the cost is nearly zero.

See [installation.md](docs/installation.md) for more information.

### Running the service

Running a service like imok for a vulnerable group is not a task to be taken lightly. It can be argued that running a bad service is worse than running no service: it can potentially give people false hope, and undermine the work of your group. Imok has been primarily designed to help improve the work of existing groups. If you do not currently operate this kind of service then it's important to have a think about what kind of service you can promise, what the protocol for responding to alerts is, and who picks up the pieces when things go wrong.

We've provided some hints and tips in [deployment.md](docs/deployment.md), and welcome contributions to this guide.

## Contributing

### Software development

We welcome contributors to help with this project. Imok is written in Django.

See [development.md](docs/development.md) for how to set up a development environment.

### Translations

Imok allows language selection for users. Currently available translations are in the [locale](locale) directory. We welcome translation into other languages.

Please note server commands in caps ('YES', 'IN', 'OUT' etc.) are not currently translatable. Please leave these in English in your translations.

[Sign up on POEditor](https://poeditor.com/projects/view?id=428751) to submit a translation.

Translations will be periodically reviewed and added to the project. If you'd like to add translations yourself see [translation.md](docs/translation.md).

## Support

We have a [Discord server](https://discord.gg/4JKak6aymM) for support and feedback.

We can also set up an installation for you for a fee. All funds raised go towards improving imok. Email [kim@gfsc.studio](mailto:kim@gfsc.studio) or join the [Discord server](https://discord.gg/4JKak6aymM) if you'd like to chat about this.

## Donations

Imok has been developed entirely by volunteers in the [Geeks for Social Change](https://gfsc.studio/) collective. If you'd like to support development, please consider sending us a one-off or regular donation.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/M4M43THUM)

## License

Imok is released under the [MIT license](LICENSE).
