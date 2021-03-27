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

## How it works (users)

## How it works (admins)

## Contributing

We welcome contributors to help with this project. Imok is written in Django.

See [development.md](docs/development.md) for how to set up a development environment.
