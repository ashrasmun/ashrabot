import os
import argparse


bot_config = None
debug      = None
_init      = False

def prepare_parser():
    parser   = argparse.ArgumentParser(add_help = False)
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # Add back help
    optional.add_argument(
        '-h',
        '--help',
        action = 'help',
        default = argparse.SUPPRESS,
        help = 'show this help message and exit',
    )

    # Required
    required.add_argument(
        '-bc',
        '--bot_config',
        help = 'JSON configuration file with defined: tmi_token, client_id,'
        ' bot_nick, bot_prefix, channel. For more information please visit:'
        ' https://dev.to/ninjabunny9000/let-s-make-a-twitch-bot-with-python-2nd8',
        required = True,
    )

    # Optional
    optional.add_argument(
        '-d',
        '--debug',
        action = 'store_true',
        help = 'enable debug level logging',
    )

    return parser.parse_args()

def validate(args):
    if not os.path.exists(args.bot_config):
        print('No such file exists (-bc/--build_config)')
        exit(1)

    if not os.path.isfile(args.bot_config):
        print('Specified path is not a file (-bc/--build_config)')
        exit(1)

    return

def expose_arguments(args):
    global bot_config
    global debug

    bot_config = args.bot_config
    debug      = args.debug

    return

def setup():
    global _init

    if _init:
        return

    args = prepare_parser()
    validate(args)
    expose_arguments(args)
    _init = True
