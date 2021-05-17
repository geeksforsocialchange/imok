# I'm OK (imok)

Imok is a simple bot to support people undertaking potentially risky activities. It's aimed at community groups who support these vulnerable people.

The bot lets users 'check in' to the service with an SMS or messaging app. If users don't 'check out' after 30 minutes (for example), it will raise an alarm in a Telegram groupchat.

Example use cases are:

- Supporting protestors at risk of arrest or kidnapping
- Supporting women and LGBTQ+ people walking home at night, or going on dates
- Supporting journalists or medical staff in warzones
- Supporting asylum seekers through 'signing in' processes (see #AbolishReporting on Twitter).

Imok is currently optimised for the latter use case. It is a collaboration between [No Borders Manchester](https://nobordersmcr.com/) and [Geeks for Social Change](https://gfsc.studio) that emerged from the [Resistance Lab](https://resistancelab.network) collective.

We do not currently offer a public instance of imok, and so you will need to set up your own server to use it. The target audience is therefore local mutual aid and community support groups with the capacity and confidence to run a web service.

We currently support SMS and Telegram. WhatsApp is theoretically supported but requires a [WhatsApp Business API account](https://www.whatsapp.com/business/api/?lang=en), which we do not have.

Please note that imok is currently **beta quality software** and has not yet been tested in a "real life" setting. We will be making rapid improvements over the coming months.

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

That's it! All server commands are listed on the [imok wiki](https://github.com/geeksforsocialchange/imok/wiki/Server-commands).

## Installation and deployment

To find out how to install imok, set up a development environment or provide translations check out the [imok wiki on GitHub](https://github.com/geeksforsocialchange/imok/wiki).

## Support

We have a [Discord server](https://discord.gg/4JKak6aymM) for support and feedback.

We can also set up an installation for you for a fee. All funds raised go towards improving imok. Email [kim@gfsc.studio](mailto:kim@gfsc.studio) or join the [Discord server](https://discord.gg/4JKak6aymM) if you'd like to chat about this.

## Donations

Imok has been developed entirely by volunteers in the [Geeks for Social Change](https://gfsc.studio/) collective. If you'd like to support development, please consider sending us a one-off or regular donation.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/M4M43THUM)

## License

Imok is released under the [MIT license](LICENSE).
