import json
import os

# Token received via https://twitchtokengenerator.com
# Go there, login as the bot and request token. Send mail with user as bot and
# mail as your mail. Then, get the Access Token from the mail.
bot_access_token = None
# https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/
bot_id           = None
bot_nick         = None
bot_prefix       = None
channel          = None

# Don't use Twitch docs or CLI. They are useless...

def load(config_path: str) -> None:
    if not os.path.isfile(config_path):
        print('Cannot find the config file!')
        return

    with open(config_path, 'r') as f:
        config = json.load(f)

    global bot_access_token
    global bot_id
    global bot_nick
    global bot_prefix
    global channel

    bot_access_token = config['bot_access_token']
    bot_id           = config['bot_id']
    bot_nick         = config['bot_nick']
    bot_prefix       = config['bot_prefix']
    channel          = [config['channel']]
