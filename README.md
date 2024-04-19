# discord2nostr
A docker container that runs a discord bot and a noscl nostr client that forwards messages from discord to nostr.

I use this to forward tweets from twitter to nostr, by having IFTTT send tweets to a discord channel, then this bot forwards to nostr from there.

## Setup

First you need to setup a discord bot and get it's token. Then change the NOSCL_PRIVATE_KEY in the dockerfile. It needs to be the hex key because nsec1 didnt seem to work for me. Then add your channel id and discord bot token to the discordbotdocker.py file. 

After adding all your info build the container with:

``` docker build -t "discord2nostr:Dockerfile" . ``` 

Then to start the container:

``` docker run --detach --restart always --name discord2nostr discord2nostr:Dockerfile ```
