# twitch-signal-emotes

This project allows you to create Signal stickers from Twitch emotes fairly easily.

## Usage

Set your Twitch API keys:

```
# For bash-like shells
export TWITCH_CLIENT_ID=your-client-id
export TWITCH_SECRET=your-secret

# For fish
set -x TWITCH_CLIENT_ID your-client-id
set -x TWITCH_SECRET your-secret
```

Then download your emotes:

```
# Emotes for the specified channel will be saved in ./out/antoinedaniel/...
./emotes.py antoinedaniel
```

```
# Specify a custom output directoy
./emotes.py antoinedaniel -o emotes
```
