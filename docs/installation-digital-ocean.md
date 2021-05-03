# Setting up imok on Digital Ocean

For this you will need a Digital Ocean account.  If you don't have one yet, please consider using our [referral link](https://m.do.co/c/34b6bc6a1cf7) which will give you more than enough credits to run this for 60 days.

## Setting up a droplet

A 'droplet' is Digital Ocean's term for a virtual server.

Anything not listed here you can just leave as it is.

1. Click **Create** in the top right corner, and then **Droplets**
1. **Choose an image**
  1. Go to 'Marketplace' tab
  1. Search for 'dokku'
  1. Select 'Dokku 0.21.4 on Ubuntu 20.04' (or whatever the latest version is)
1. **Choose a plan:** 'Basic', 'Regular intel with SSD', '$5/mo'
1. **Choose a datacentre region:** pick whichever datacentre is closest to you
1. **Authentication:** we recommend using an SSH key method if you are able to follow the instructions in the interface. If not then a password is totally fine but make it a strong one, ideally using a strong password generator.
1. **Choose a hostname:** pick a memorable name for the server
1. **Enable backups:** this is up to you but we recommend it
1. Click **'Create Droplet'** and you're done!

## Signing into the droplet

You will then see a list of droplets in your interface. Give it a second while it sets up your new droplet.

1. Copy the IP address (e.g. 123.123.123.123)
1. In the terminal on your computer, type `ssh root@YOUR_IP`. Type 'yes' when it asks you if you want to proceed.

You can now return to the main [installation instructions](installation.md) where you left off.
