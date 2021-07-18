import os
import greeting

from twitchio.ext import commands
from details import config


print('Reading configuration...')
config.load('config.json')

bot = commands.Bot(
    irc_token        = config.tmi_token,
    client_id        = config.client_id,
    nick             = config.bot_nick,
    prefix           = config.bot_prefix,
    initial_channels = config.channel,
)

@bot.event
async def event_ready():
    """Called once when the bot goes online."""
    print(f'{config.bot_nick} is online!')
    ws = bot._ws # allow bot to send messages during this event

    message = f'/me is online, {greeting.get_a_bop()}'
    await ws.send_privmsg(config.channel[0], message)

index = 0

@bot.event
async def event_message(context):
    """Runs every time a message is sent in chat."""
    # TODO:
    # Reset the index when the 30s timer cools down.

    # make sure the bot ignores itself and the streamer
    if context.author.name.lower() == config.bot_nick.lower():
        return

    content = context.content.lower()

    if content.find('mus') != -1:
        global index
        paren = '' if index == 0 else f' ({index})'
        index = index + 1
        await context.channel.send(f'mus KEKW{paren}')

async def _print_context(context):
    print(dir(context))
    print(context.color)
    print(context.author)
    print(context.command)
    print(dir(context.command))
    print(context.content)
    print(context.kwargs)
    print(context.message)
    print(dir(context.message))
    print(context.prefix)

@bot.command(name='lurk')
async def lurk(context):
    """
    TODO:
        1. Figure out why the username is always in lowercase instead of
        original case.
        2. Make the command case insensitive - if possible, of course.
    """
    args = context.content.split(' ')
    args.pop(0)
    reason = ' '.join(args) if args else 'your lurking'
    await context.send(f'Enjoy {reason}, {context.author.name} peepoLove')

#TODO
# Add command to ban bots:
#Wanna become famous? Buy followers, primes and viewers on cutt.ly/xxxxxx ( bigfollows . com )!

if __name__ == '__main__':

    print('Starting the bot...')
    bot.run()
