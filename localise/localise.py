#!/usr/bin/env python
import argparse
import signal
import sys
import os
from colorama import init, Fore, Back, Style

try:
    from .commands import *
    from .helper import *
except SystemError:
    from commands import *
    from helper import *

class ConfigException(Exception):
    """Raise when config file is invalid"""

def signal_handler(caught_signal, frame):
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
    if hasattr(args, 'config_file') and args.config_file:
        config_file = args.config_file

    if not os.path.isfile(config_file):
        print(Fore.RED + 'No configuration file found! Run the following command to create one:' + Style.RESET_ALL)
        print('')
        print('    localize config')
        print('')
        print('You can also create the file manually in your $HOME directory: $HOME/.localise/config.yml')
        print('')
        sys.exit(1)

    with open(config_file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    return cfg


def command(args):
    if not args.command == 'config':
        try:
            configuration = get_configuration(args)
        except ConfigException as e:
            print(str(e))
            sys.exit(1)

    try:
        if args.command == 'list':
            print("Available projects:")
            for section in configuration:
                print(section)
        elif args.command == 'push':
            check_config_section(configuration, args, args.project)
            push(configuration[args.project], args)
        elif args.command == 'pull':
            check_config_section(configuration, args, args.project)
            pull(configuration[args.project], args)
        elif args.command == 'config':
            config(args)
        else:
            print_error("Not a valid command \"%s\"! Did you mean config, push, or pull?" % (args.command))
            sys.exit(1)
        sys.exit(0)
    except ConfigException as e:
        print(str(e))
        sys.exit(1)
    except OperationException as e:
        print(str(e))
        sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(description='Localise')
    parser.add_argument('command', nargs='?', help='Specify command: push, pull, config')
    parser.add_argument('project', nargs='?', default='default', help='Specify project name')

    parser.add_argument("-c", "--config", dest="config_file", help="Specify config file", metavar="FILE")
    parser.add_argument("-t", "--token", dest="token", help="Specify token")
    parser.add_argument('--verbose', '-v', action='count')

    args = parser.parse_args()

    return args


def main():
    init(autoreset=True)
    args = parse_args()
    command(args)

def check_config_section(cfg, args, section):
    if not section in cfg:
        raise ConfigException('Unknown project identificator "%s". Check that your config is in project parent.' % (section))
    try:
        token = cfg[section]['api']['token']
        if not token:
            raise TypeError('Empty token')
    except (KeyError, TypeError):
        token = None  # or whatever
        if not args.token:
            raise ConfigException('Missing token value in config file')
    if not 'translations' in cfg[section] or not cfg[section]['translations']:
        raise ConfigException('No translation files defined in config file')

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
