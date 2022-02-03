import sys
import greeting
import random
import asyncio
import subprocess
import shlex
import twitchio
import json

from twitchio.ext import commands, pubsub
from details import config, args


class AshraBot(commands.Bot):
    def __init__(self, *_args, **_kwargs):
        super().__init__(*_args, **_kwargs)
        self.mus_index      = 0
        self.corvibot_index = 0
        self.channel_name   = _kwargs.get('initial_channels')[0]
        assert self.channel_name

        with open(args.blocked_words) as f:
            loaded_json = json.load(f)
            self.blocked_words = loaded_json.get('words')

    async def check(self, what: str):
        """Debug method used to check various stuff"""
        assert self.channel, (
            "Channel name should be cached upon bot going online"
        )
        await self.channel.send('PepoG I need to check something...')
        print(what)
        await self.channel.send('MrDestructoid Boss, look at my console!...')

    # -------------------------------- Events ------------------------------- #

    async def event_ready(self):
        """Called once when the bot goes online."""
        print(f'{config.bot_nick} is online!')
        self.channel = self.get_channel(self.channel_name)
        message = f'/me is online, {greeting.get_a_bop()}'
        await self.channel.send(message)

    def _react_to_mus(self):
        # Make sure the new message is unique
        paren = '' if self.mus_index == 0 else f' ({self.mus_index})'
        self.mus_index = self.mus_index + 1
        return f'mus KEKW{paren}'

    def _react_to_corvibot(self):
        # Make sure the new message is unique
        paren = '' if self.corvibot_index == 0 else f' ({self.corvibot_index})'
        self.corvibot_index = self.corvibot_index + 1
        return f'peepoLove{paren}'

    async def event_message(self, message):
        """Runs every time a message is sent in chat."""
        # TODO:
        # Reset the index when the 30s timer cools down.

        # I have no idea why this can be a thing :(
        if not message.author:
            return

        # Make sure the bot ignores itself and the streamer
        if message.author.name.lower() == config.bot_nick.lower():
            return

        # Cache the channel
        self.channel = message.channel

        # Handle commands with prefix
        await self.handle_commands(message = message)

        content       = message.content.lower()
        split_content = content.split(' ')

        if 'mus' in split_content:
            content = self._react_to_mus()
        elif 'corvibot' in split_content:
            content = self._react_to_corvibot()
        else:
            return

        await message.channel.send(content)

    async def event_usernotice_subscription(self, metadata):
        """
        React to subscriptions.

        TODO: test it :)
        """
        thanks = [
            'FeelsOkayMan 🍷, thanks kind Sir/Madamme!',
            'HYPER yay, thanks!',
            'Pog WHAT A MADLAD!',
            'PeepoGlad I appreciate your help!'
        ]

        chosen = thanks[random.randint(0, len(thanks))]
        await metadata.channel.send(chosen)
        # await self.check(dir(metadata))

    # ------------------------------ Commands ------------------------------- #

    @commands.command(name = "lurk")
    async def lurk_command(self, context):
        """
        TODO:
            1. Figure out why the username is always in lowercase instead of
            original case.
            2. Make the command case insensitive - if possible, of course.
        """
        args = context.message.content.split(' ')
        args.pop(0)
        reason = ' '.join(args) if args else 'your lurking'

        if reason == 'me':
            await context.send(f'Enjoy m... wait, what? monkaS')
            return

        await context.send(f'Enjoy {reason}, {context.author.name} peepoLove')

    @commands.command(name = "discord")
    async def discord_command(self, context):
        """Inform about discord server"""
        await context.send('Please check the channel\'s description'
                           f' {context.author.name} peepoHappy')

    @commands.command()
    async def hello(self, context):
        # Send a hello back!
        await context.send(f'Hello {context.author.name}!')

    @commands.command()
    async def corvibot(self, context):
        content = self._react_to_corvibot()
        await context.send(content)

    def _sanitize_tts_content(self, content: str) -> str:
        """Changes the message into a caution when a blocked word is
        encountered"""

        for word in content.split(' '):
            for blocked in self.blocked_words:
                if blocked.lower() in word.lower():
                    return 'No no, very naughty!'

        return content

    def _construct_tts_command(self, raw_command: str) -> str:
        """Accepts raw content from the twitch chat and returns a properly
        formed PowerShell command"""
        content = raw_command.split(' ')
        content = ' '.join(content[1:])
        content = self._sanitize_tts_content(content)
        command = f'PowerShell -File tts/tts.ps1 -TextToSay "{content}"'
        return shlex.split(command)

    # For testing purposes
    @commands.command(name = 'tts')
    async def tts_command(self, context):
        subprocess.run(self._construct_tts_command(context.message.content))
        await context.send('Transcribulating PepoG ...')


def main():
    print(f'I\'m running using: {sys.executable}')
    print('Reading configuration...')
    config.load(args.bot_config)

    bot = AshraBot(
        token            = config.tmi_token,
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
