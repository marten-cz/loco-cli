#!/usr/bin/env python
import sys
import yaml
import os
import requests
import json

from six.moves import input

try:
    from .helper import *
except SystemError:
    from helper import *

def get_url(conf):
    return 'https://localise.biz/api/'


def config(args):
    from os.path import expanduser
    home = expanduser("~")
    config_file = home + '/.localise/config.yml'
    if hasattr(args, 'config_file') and args.config_file:
        config_file = args.config_file

    print("Create config file in %s" % (config_file))

    token = input('Localise API token [None]: ')

    data = dict(
        default=dict(
            api=dict(
                token=token
            ),
            translations=[
                dict(
                    locale='en-US',
                    format='po',
                    file='/tmp/locale/en/messages.po'
                )
            ],
            push={
                "index": 'id',
                "ignore-new": 'false',
                "ignore-existing": 'false',
                "delete-absent": 'false'
            },
            pull=dict(
            )
        )
    )

    if not os.path.exists(os.path.dirname(config_file)):
        os.makedirs(os.path.dirname(config_file))
    with open(config_file, 'w+') as out:
        out.write(yaml.dump(data, default_flow_style=False))


def push(conf, args):
    errors = []

    if 'translations' not in conf:
        raise OperationException('Could not find any translations to pull. Please make sure your configuration is formed correctly.')

    for translation in conf['translations']:
        if 'locale' not in translation or 'format' not in translation or 'file' not in translation:
            raise OperationException('Missing translation data.')

        try:
            with open(translation['file']) as translation_file:
                file = translation_file.read()
        except (IOError, OSError) as e:
            errors.append('Error: ' + str(e))
            break
        token = getattr(args, 'token')
        if not token:
            token = conf['api']['token']

        params = conf['push']
        params.update(dict(
            key=token,
            locale=translation['locale']
        ))
        url = get_url(conf) + 'import/%s' % (translation['format'])

        response = requests.post(url, params=params, data=file)
        if response.status_code == 401:
            errors.append('Invalid API key in config file')
        elif response.status_code != 200:
            message = 'Something went wrong. Please contact support.'
            res = json.loads(response.text)
            if 'error' in res and res['error']:
                message = res['error'] + ' for file ' + translation['file']

            errors.append(message)

    # If there are any errors display them to the user
    if errors:
        for error in errors:
            print(Fore.RED + error + Style.RESET_ALL)
        raise OperationException()
    else:
        print_success('Successfully pushed ' + str(len(conf['translations'])) + ' file(s) to Localise.biz!')


def pull(conf, args):
    errors = []

    if 'translations' not in conf:
        raise OperationException('Could not find any translations to pull. Please make sure your configuration is formed correctly.')

    for translation in conf['translations']:
        if not 'locale' in translation or not 'format' in translation or not 'file' in translation:
            raise OperationException('Missing translation data.')

        url = get_url(conf) + 'export/locale/%s.%s?format=%s' % (
            translation['locale'], translation['format'], translation['format'])

        token = getattr(args, 'token')
        if not token:
            token = conf['api']['token']
        response = requests.get(url, stream=True, auth=(token, ''))

        if response.status_code == 401:
            errors.append('Invalid API key in config file')
        elif response.status_code != 200:
            message = 'Something went wrong.'
            try:
                res = json.loads(response.text)
                if res['meta']['error']['message']:
                    message = res['meta']['error']['message'] + ' for file ' + translation['file']
            except (ValueError) as e:
                message = 'Wrong response format'
                if hasattr(args, 'verbose') and args.verbose > 0:
                    errors.append(response.text)

            errors.append(message)
        else:
            # Swap put the content of the file with the data
            with open(translation['file'], 'wb') as translation_file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        translation_file.write(chunk)

    # If there are any errors display them to the user
    if errors:
        for error in errors:
            print_error(error + Style.RESET_ALL)
        raise OperationException()

    else:
        print_success('Successfully pulled ' + str(len(conf['translations'])) + ' file(s) from Localise.biz!')

