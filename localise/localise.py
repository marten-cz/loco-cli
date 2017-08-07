#!/usr/bin/env python

import argparse
from colorama import init, Fore, Back, Style
from commands import *
import signal
import sys

class ConfigException(Exception):
    """Raise when config file is invalid"""

def signal_handler(signal, frame):
    print("\nInterrupted!")
    sys.exit(0)

def get_configuration(args):
    """
    Parse configuration file

    Throw an exception when file does not exists or has wrong format.
    :param args:
    :return:
    """
    from os.path import expanduser
    home = expanduser("~")
    config_file = home + '/.localise/config.yml'
    if hasattr(args, 'config_file'):
        config_file = args.config_file

    if not os.path.isfile(config_file):
        print(Fore.RED + 'No configuration file found! Run the following command to create one:' + Style.RESET_ALL)
        print('')
        print('    localize config')
        print('')
        print('You can also create the file manually in your $HOME directory: $HOME/.localise/config.yml')
        print('')
        sys.exit()

    with open(config_file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    if not 'api' in cfg or not 'token' in cfg['api'] or not cfg['api']['token']:
        raise ConfigException('Missing token value in config file')
    if not 'translations' in cfg:
        raise ConfigException('No translation files defined in config file')

    return cfg


def command(args):
    if not args.command == 'config':
        try:
            configuration = get_configuration(args)
        except ConfigException as e:
            print(e.message)
            return

    if args.command == 'push':
        push(configuration, args)
    elif args.command == 'pull':
        pull(configuration, args)
    elif args.command == 'config':
        config(args)
    else:
        sys.exit(Fore.RED + "Not a valid command \"%s\"! Did you mean config, push, or pull?" % (
        args.command) + Style.RESET_ALL)


def parse_args():
    p = argparse.ArgumentParser(description='Localise')
    p.add_argument('command', nargs='?', help='Specify command: push, pull, config')

    p.add_argument("-c", "--config", dest="config_file", help="Specify config file", metavar="FILE")
    p.add_argument('--verbose', '-v', action='count')

    args = p.parse_args()

    return args


def main():
    init(autoreset=True)
    args = parse_args()
    command(args)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
