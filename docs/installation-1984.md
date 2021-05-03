[1984](https://www.1984.is/) are independent and based in Iceland.  They use 100% green energy and strong on privacy and civil rights.  We have no relationship with them, but they are recommended from many sources.

While GFSC do not advocate the use of cryptocurrency for environmental reasons, if you are absolutely determined to conceal your identity you can pay for 1984 services anonymously with Bitcoin or Monero.  Obtaining and paying with Bitcoin or Monero is out of scope for this document.

Unlike [Digital Ocean](installation-digital-ocean.md), 1984 do not provide a pre-configured Dokku server.  So the work is slightly more involved.

To switch to English language pages, click on the flag at the top right of the page.

### Setting up a VPS

Once you have an account and are logged into the control panel, switch the currency to your preferred option and look for VPS #1.  This is their cheapest offering and should be more than enough to run your instance of imok.

Choose a memorable hostname

Choose "Debian GNU/Linux Buster - 2020-08-05" (or a newer option if available)

You can set a root password to login with (which will let you use the web console), but it is better to use SSH keys instead if you can do that.

Agree to the terms of service and add to the cart

You'll be asked to configure a billing contact if you haven't already created one.  Select your preferred currency and fill in the remaining details.

The server takes a few minutes to create, so this is a good point to go and get a coffee.

### Signing into the server

Click on the VPS Control button in your Overview page

If you have set a root password then you can click to access the console, press enter a few times, and you will be asked to login.  Provide the username `root` and the password you configured.

If you only set an ssh key (or want to use the commandline), then ssh in to the server from your machine.  Copy the network address and in your terminal type `ssh root@YOUR_SERVER_IP`

### Configuring Dokku

Edit /etc/hosts to set the hostname you chose when creating the server.  The first line should look something like the following (replacing myserver.example.com with your server's name)

```
127.0.0.1 localhost myserver.example.com
```

Perform the main installation of Dokku.  This will take a few minutes but any errors will usually happen immediately.

```shell
wget https://raw.githubusercontent.com/dokku/dokku/v0.24.7/bootstrap.sh;
DOKKU_TAG=v0.24.7 bash bootstrap.sh
```

You can now continue with the rest of the [installation instructions](installation.md).
