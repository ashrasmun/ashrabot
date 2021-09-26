import json
import os


tmi_token  = None
client_id  = None
bot_nick   = None
bot_prefix = None
channel    = None


def load(config_path: str) -> None:
    if not os.path.isfile(config_path):
        print('Cannot find the config file!')
        return

    with open(config_path, 'r') as f:
        config = json.load(f)

    global tmi_token
    global client_id
    global bot_nick
    global bot_prefix
    global channel

    tmi_token  = config['TMI_TOKEN']
    client_id  = config['CLIENT_ID']
    bot_nick   = config['BOT_NICK']
    bot_prefix = config['BOT_PREFIX']
    channel    = [config['CHANNEL']]
