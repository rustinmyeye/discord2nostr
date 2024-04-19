#!/bin/bash

# Set the private key from the environment variable NOSCL_PRIVATE_KEY
./noscl setprivate $NOSCL_PRIVATE_KEY

# Add relays using environment variables
./noscl relay add $RELAY_URL1
./noscl relay add $RELAY_URL2
./noscl relay add $RELAY_URL3
./noscl relay add $RELAY_URL4
./noscl relay add $RELAY_URL5
./noscl relay add $RELAY_URL6
# Add more 'noscl relay add' lines for additional relay URLs if needed

# Execute the Discord bot script
python discordbotdocker.py
