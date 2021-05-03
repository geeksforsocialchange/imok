# Setting up an imok server in the real world

## Thinking about security

Imok, to the best of our knowledge, is completely legal in the UK. You are well within your rights to run and operate and instance of it for any purpose you like. However, with the current 'hostile environment' and the rise of the far right, it's wise to take security precautions to ensure the safety of everyone involved.

The three main threats to your instance that imok have been designed with in mind are:

- Attempts to hack into the server to dox vulnerable people by the far right.
- Seizure of the server by the police or security services to get a list of users.
- Infiltration of your group by either of the above to get the same information.

We believe that in all cases there are _far_ easier ways to get this information than imok, which fundamentally holds almost no data for the amount of effort this would take. However, here's some tips that we highly recommend you read and absorb before proceeding with a full rollout.

1. Have as few people as possible with actual server access (preferably exactly one).
1. Have as few people as possible with access to the admin interface (preferably no more than two).
1. Make a plan to periodically remove people from the admin Telegram group that are no longer active in the group.
1. Ensure every admin has at at least an eight digit security password on their phone. Fingerprints have been coerced in at least one case, and patterns are easy to guess. Remember that you are only as secure as your weakest link.
1. Enable 'disappearing messages' on the admin Telegram group.
1. Telegram invite links work until they are cancelled. Revoke the invite link for the admin group whenever you are not actively expecting new admins to join.
1. If possible set up your server in a country with good privacy laws. We recommend Iceland or Switzerland. Anywhere that's not the UK is great though -- just make it a hassle.
1. SMS is provided as a fallback but you should be aware that SMS messages can be intercepted, that every SMS will be very easy to trace, and that they can be spoofed by security services to create a false 'out' message. Obviously it is highly unlikely that these will be serious concerns in almost all instances.

## Running a pilot

Before rolling out properly we recommend running a limited pilot with people you already know. The details will be up to your specific use case but some things to consider are:

- An agreement over who is managing the server and installing updates on it, where passwords are stored, where Airbrake messages get sent to, and what happens if this person leaves the group suddenly.
- Creation of a shared 'runbook', detailing processes such as adding new members, what happens if something breaks, what happens if a phone gets seized, etc. This can be created organically to some extent as you go.
- Consider setting up a phone number for new member requests that's not tied to your imok install at all. That way, you can vet new members before adding them to your system. It's extremely hard to break into a server if you don't even know where it is!
- Publishing an SLA. Remember you're all human, and likely doing this in your spare time. It's good to consider what promises you make to members and how you will stick to that.

## Let us know how you get on

If it's safe for you to do so, we welcome improvements and changes to these docs. Raise a pull request or email kim@gfsc.studio with any suggestions.
