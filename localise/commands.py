#!/usr/bin/env python

import sys
import yaml
import os
import requests
import json

from colorama import Fore, Back, Style


def get_url(conf):
    return 'https://localise.biz/api/'


def config():
    token = raw_input('Localise API token [None]: ')

    data = dict(
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

    from os.path import expanduser
    home = expanduser("~")
    config_file = home + '/.localise/config.yml'

    if not os.path.exists(os.path.dirname(config_file)):
        os.makedirs(os.path.dirname(config_file))
    with open(config_file, 'w+') as out:
        out.write(yaml.dump(data, default_flow_style=False))


def push(conf):
    errors = []

    if not 'translations' in conf:
        sys.exit(
            Fore.RED + 'Could not find any translations to pull. Please make sure your configuration is formed correctly.' + Style.RESET_ALL)

    for translation in conf['translations']:
        if not 'locale' in translation or not 'format' in translation or not 'file' in translation:
            sys.exit(Fore.RED + 'Missing translation data.' + Style.RESET_ALL)

        try:
            with open(translation['file']) as f:
                file = f.read()
        except (IOError, OSError) as e:
            errors.append('Error: ' + str(e))
            break

        params = conf['push']
        params.update(dict(
            key=conf['api']['token'],
            locale=translation['locale']
        ))
        url = get_url(conf) + 'import/%s' % (translation['format'])

        r = requests.post(url, params=params, data={'src': file})
        if r.status_code != 200:
            message = 'Something went wrong. Please contact support.'
            res = json.loads(r.text)
            if r['error']:
                message = res['error'] + ' for file ' + translation['file']

            errors.append(message)

    # If there are any errors display them to the user
    if errors:
        for error in errors:
            print(Fore.RED + error + Style.RESET_ALL)
    else:
        sys.exit(Fore.GREEN + 'Successfully pushed ' + str(
            len(conf['translations'])) + ' file(s) to Localise.biz!' + Style.RESET_ALL)


def pull(conf):
    errors = []

    if not 'translations' in conf:
        sys.exit(
            Fore.RED + 'Could not find any translations to pull. Please make sure your configuration is formed correctly.' + Style.RESET_ALL)

    for translation in conf['translations']:
        if not 'locale' in translation or not 'format' in translation or not 'file' in translation:
            sys.exit(Fore.RED + 'Missing translation data.' + Style.RESET_ALL)

        url = get_url(conf) + 'export/locale/%s.%s?format=%s' % (
            translation['locale'], translation['format'], translation['format'])

        r = requests.get(url, stream=True, auth=(conf['api']['token'], ''))

        if r.status_code != 200:
            message = 'Something went wrong.'
            res = json.loads(r.text)
            if res['meta']['error']['message']:
                message = res['meta']['error']['message'] + ' for file ' + translation['file']

            errors.append(message)
        else:
            # Swap put the content of the file with the data
            with open(translation['file'], 'wb') as file:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

    # If there are any errors display them to the user
    if errors:
        for error in errors:
            print(Fore.RED + error + Style.RESET_ALL)
    else:
        sys.exit(Fore.GREEN + 'Successfully pulled ' + str(
            len(conf['translations'])) + ' file(s) from Localise.biz!' + Style.RESET_ALL)
