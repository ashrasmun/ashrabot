import sys
import greeting

from twitchio.ext import commands
from details import config, args


index = 0


class AshraBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def event_ready(self):
        """Called once when the bot goes online."""
        print(f'{config.bot_nick} is online!')
        ws = self._ws  # allow bot to send messages during this event

        message = f'/me is online, {greeting.get_a_bop()}'
        await ws.send_privmsg(config.channel[0], message)

    async def event_message(self, context):
        """Runs every time a message is sent in chat."""
        # TODO:
        # Reset the index when the 30s timer cools down.

        # Make sure the bot ignores itself and the streamer
        if context.author.name.lower() == config.bot_nick.lower():
            return

        content       = context.content.lower()
        split_content = content.split(' ')

        # Make sure the new message is unique
        global index
        paren = '' if index == 0 else f' ({index})'
        index = index + 1

        if 'mus' in split_content:
            content = f'mus KEKW{paren}'
        elif 'corvibot' in split_content:
            content = f'peepoLove{paren}'
        else:
            return

        await context.channel.send(content)

    async def _print_context(self, context):
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

    @commands.command(name = "lurk")
    async def lurk_command(self, context):
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

    @commands.command()
    async def hello(self, ctx):
        # Send a hello back!
        await ctx.send(f'Hello {ctx.author.name}!')


def main():
    print(f'I\'m running using: {sys.executable}')
    print('Reading configuration...')
    config.load(args.bot_config)

    bot = AshraBot(
        irc_token        = config.tmi_token,
        client_id        = config.client_id,
        nick             = config.bot_nick,
        prefix           = config.bot_prefix,
        initial_channels = config.channel,
    )

    # TODO
    # Add command to ban bots:
    # Wanna become famous? Buy followers, primes and viewers on cutt.ly/xxxxxx
    # ( bigfollows . com )!

    print('Starting the bot...')
    bot.run()


if __name__ == '__main__':
    args.setup()
    main()
