#!/usr/bin/env python

import argparse
from colorama import init, Fore, Back, Style
from commands import *
import signal
import sys

def signal_handler(signal, frame):
    print("\nInterrupted!")
    sys.exit(0)

def get_configuration(args):
    from os.path import expanduser
    home = expanduser("~")
    config_file = home + '/.localise/config.yml'
    if hasattr(args, config_file):
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

    return cfg


def command(args):
    if not args.command == 'config':
        configuration = get_configuration(args)

    if args.command == 'push':
        push(configuration)
    elif args.command == 'pull':
        pull(configuration)
    elif args.command == 'config':
        config(args)
    else:
        sys.exit(Fore.RED + "Not a valid command \"%s\"! Did you mean config, push, or pull?" % (
        args.command) + Style.RESET_ALL)


def parse_args():
    p = argparse.ArgumentParser(description='Localise')
    p.add_argument('command', nargs='?', help='an integer for the accumulator')

    p.add_argument("-c", "--config", dest="config_file", help="Specify config file", metavar="FILE")

    args = p.parse_args()

    return args


def main():
    init(autoreset=True)
    args = parse_args()
    command(args)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
