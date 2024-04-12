import sys
import greeting
import random
import subprocess
import shlex
import json
import re
import os

from datetime import datetime
from twitchio.ext import commands, pubsub, sounds
from details import config, args, handlers


class AshraBot(commands.Bot):
    def __init__(self, *_args, **_kwargs):
        super().__init__(*_args, **_kwargs)
        self.mus_index      = 0
        self.corvibot_index = 0
        self.player = sounds.AudioPlayer(callback = self.player_done)

        if (c := _kwargs.get('initial_channels')) and len(c) > 0:
            self.channel_name = c[0]
            assert self.channel_name

        with open(args.blocked_words) as f:
            loaded_json = json.load(f)
            self.blocked_words = loaded_json.get('words')

        bannable_phrases_raw = [
            'wanna become famous. buy viewers. followers and primes.*',
            'Wanna become famous. Buy followers. primes and viewers on yourfollowz. com.*',
            '.*I want to offer promotion of your channel.*',
        ]
        self.bannable_phrases = [re.compile(p, re.I) for p in bannable_phrases_raw]

    async def send(self, context, message: str):
        print(message)
        await context.send(message)

    async def player_done(self):
        pass

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
        assert self.channel, 'Noone\'s on the channel'
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

    async def _handle_spam_bots(self, message):
        content = message.content.lower()

        for phrase in self.bannable_phrases:
            if phrase.search(content):
                author = message.author.name
                print(f"Bot detected: {author}")
                await message.channel.send(f"@ashrasmun Boss, something's sus here ConcernFroge ({author})")

    async def _handle_timeout(self, message):
        if not self._contains_blocked_word(message.content):
            return

        username = message.author.name
        # username = 'autobot_ryan'  # for testing :)
        duration = 10  # in seconds
        reason   = 'Please refrain from using such words - it\'s against TOS.'\
            ' This timeout is automatic. If you feel the word you used'\
            ' shouldn\'t be blocked, tell the streamer about it. ~ashrabot'
        await message.channel.send(f'/timeout {username} {duration} {reason}')
        print(f'{username} was timed out because they wrote: {message.content}')

    async def _handle_silly_jokes(self, message):
        split_content = message.content.lower().split(' ')

        def has_co(words: list[str]):
            for word in words:
                if 'co?' in word:
                    return True

            return False

        if 'mus' in split_content:
            content = self._react_to_mus()
        elif 'corvibot' in split_content:
            content = self._react_to_corvibot()
        elif has_co(split_content):
            content = 'wiaderko 🤭'
        else:
            return

        await message.channel.send(content)

    async def event_message(self, message):
        """Runs every time a message is sent in chat."""
        # TODO:
        # Reset the index when the 30s timer cools down.

        # I have no idea why this can be a thing :(
        if not message.author:
            return

        # Make sure the bot ignores itself
        if type(message.author.name) is str:
            name = message.author.name

            if name.lower() == config.bot_nick.lower():
                return

        # Cache the channel
        self.channel = message.channel

        # TODO: Separate script cannot interact with Twitch, so after sending
        # data to a separate process, we'll need to wait until the data is
        # properly prepared by the external process and then it can be read by
        # the actual bot.
        #
        # # Handle commands with prefix
        # if message:
        #     words = message.content.split()
        #     is_command = len(words) > 1 and words[0].startswith("!")

        #     if is_command:
        #         print("is_command")
        #         cmd = f'py details/handlers.py "{message.content}"'
        #         print(cmd)
        #         subprocess.run(cmd)

        await self.handle_commands(message = message)

        await self._handle_spam_bots(message)
        await self._handle_timeout(message)
        await self._handle_silly_jokes(message)

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

    def _contains_blocked_word(self, content: str) -> bool:
        for word in content.split(' '):
            for blocked in self.blocked_words:
                if blocked.lower() in word.lower():
                    return True

        return False

    def _sanitize_tts_content(self, content: str) -> str:
        """Changes the message into a caution when a blocked word is
        encountered"""

        return 'No no, very naughty!' \
               if self._contains_blocked_word(content) \
               else content

    def _construct_tts_command(self, raw_command: str) -> list[str]:
        """Accepts raw content from the twitch chat and returns a properly
        formed PowerShell command"""
        content = raw_command.split(' ')
        content = ' '.join(content[1:])
        content = self._sanitize_tts_content(content)
        command = f'PowerShell -File tts/tts.ps1 -TextToSay "{content}"'
        return shlex.split(command)

    @commands.command(name = 'tts')
    async def tts_command(self, context):
        subprocess.run(self._construct_tts_command(context.message.content))
        await context.send('Transcribulating PepoG ...')

    @commands.command(name = 'beach_mouse', aliases = ['beach', 'mouse'])
    async def beach_mouse_command(self, context):
        beach_mouse = 'beach, mouse, beach beach mouse, pxichxijchpxichxijchpxichxijchpxichxijch beach, mouse, beach beach mouse, pxichxijchpxichxijchpxichxijchpxichxijch'
        await context.send('That\'s my jam EZ')
        subprocess.run(self._construct_tts_command(beach_mouse))

    @commands.command(name = 'emoteamid')
    async def stompamid_command(self, context):
        words = context.message.content.split()

        if len(words) < 3:
            await context.send('Hey! You need to specify name of the emote to '
                    'display and the emoteamid\'s height, for example: '
                    '!emoteamid PeepoGlad 4')
            return

        user_emote = words[1]
        user_count = words[2]

        count          = int(user_count) if user_count.isdigit() else 1
        count          = count if count > 0 else 1
        maximum_height = 4

        if count > maximum_height:
            await context.send(f'Forget about it WTFFF (maximum height is {maximum_height})')
            return

        text = user_emote + ' '

        counter   = 1
        increment = 1

        for _ in range(2 * count - 1):
            await context.send(text * counter)
            counter = counter + increment

            if counter == count:
                increment = -1

    @commands.command(name = 'valheim')
    async def valheim_command(self, context):
        options = ('mods', 'hc',)
        words = context.message.content.split()

        def matches(command_name: str):
            return words and len(words) > 1 and words[1] == command_name

        if matches(options[0]):
            p = r"C:\Program Files (x86)\Steam\steamapps\common\Valheim\BepInEx\plugins"
            plugins = [d.name for d in os.scandir(p) if d.is_dir()]

            def trim(name: str):
                match = re.search(r"[-\d]", name)
                return name[:match.start()] if match else name

            plugins = [trim(p) for p in plugins]
            rationale = (
                'The rationale is to make the game less tedious in some areas'
                ' and to make it slightly more exciting by introducing more'
                ' difficult monsters and fancy magic items'
            )
            num_of_plugs = len(plugins) + 1
            repr_plugs = ', '.join(plugins)

            await context.send(
                f'Currently there are {num_of_plugs} mods used, which are: '
                f'{repr_plugs} and BepInEx'
            )
            await self.send(context, rationale)
            return

        if matches(options[1]):
            await self.send(context, 'Current world uses these options:')
            await self.send(context, 'https://i.imgur.com/AKuGq7k.png')
            await self.send(context, 'Death = new world')
            return

        presented_options = ', '.join(options)
        await self.send(context,
            f"Available options are: {presented_options}. For example "
            "'!valheim mods'"
        )

    async def _create_quote(self, words: list[str]) -> str:
        if not words:
            return ""

        quote = words[1:] if len(words) > 1 else ""

        if not quote:
            return ""

        pres_quote = ' '.join(quote)
        today = datetime.today().strftime("%y-%m-%d %H:%M:%S")
        return f'"{pres_quote}" ~ashra {today}'

    @commands.command(name = 'addquote')
    async def addquote_command(self, context):
        words = context.message.content.split()
        quote = self._create_quote(words)

        quotes_file = 'quotes.txt'

        # Ensure the file exists
        if not os.path.isfile(quotes_file):
            with open(quotes_file, 'w'):
                pass

        # TODO:
        # 0. clean up the quote from any non-ascii character or simply reject
        # the quote
        # 1. read file and see how many quotes are already there
        # 2. use the last number and append the command

        #with open(quotes_file, 'r'):


    @commands.command(name = 'quote')
    async def quote_command(self, context):
        # TODO:
        # read the quote based on number - maybe fuzzy search?
        # print help otherwise
        pass

    @commands.command(name = 'commands')
    async def display_command(self, context):
        available = [
            'lurk',
            'discord',
            'hello',
            'corvibot',
            'tts',
            'beach_mouse',
            'valheim',
            'addquote'
        ]
        formatted = ','.join(available)
        await context.send(f'Available commands are {formatted}')

args.setup()
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

bot.pubsub = pubsub.PubSubPool(bot)

@bot.event()
async def event_pubsub_channel_points(event: pubsub.PubSubChannelPointsMessage):
    if event.reward.title == "Grzegorz":
        bot.player.play(
            sounds.Sound(source = r'f:\Media\twitch\grzegorz\grzegorz.mp3')
        )
        return

@bot.event()
async def event_ready():
    topics = [
        pubsub.channel_points(config.user_token)[config.user_id]
    ]
    await bot.pubsub.subscribe_topics(topics)

print('Starting the bot...')
# TODO: ensure that working directory is the one in which the script lives for
# the duration of the bot's lifetime
bot.run()

