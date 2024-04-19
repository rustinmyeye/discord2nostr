# Use the official Python image as the base image
FROM python:3.9-slim

# Install Go
RUN apt-get update && apt-get install -y golang

# Clone the 'noscl' repository and install 'noscl'
RUN go install github.com/fiatjaf/noscl@latest

# Set the working directory
WORKDIR /app

# Move the noscl executable to the working directory and set execute permissions
RUN mv /root/go/bin/noscl /app/noscl && chmod +x noscl

# Copy the necessary files into the container
COPY discordbotdocker.py .
COPY entrypoint.sh .
COPY config.json .

# Install required Python packages
RUN pip install discord.py

# Create the Nostr configuration directory
RUN mkdir -p /root/.config/nostr

# Set the environment variable for the Nostr configuration file path
ENV NOSCL_CONFIG_PATH=/root/.config/nostr/config.json

# Set environment variables for noscl configuration
ENV NOSCL_PRIVATE_KEY=<add private nostr key here in hex format... nsec1 doesnt work>
ENV RELAY_URL1=wss://relay.snort.social
ENV RELAY_URL2=wss://relay.shitforce.one
ENV RELAY_URL3=wss://offchain.pub
ENV RELAY_URL4=wss://eden.nostr.land
ENV RELAY_URL5=wss://relay.damus.io
ENV RELAY_URL6=wss://nos.lol
# Add more environment variables for additional relay URLs if needed

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Set the entrypoint for the container
ENTRYPOINT ["./entrypoint.sh"]
