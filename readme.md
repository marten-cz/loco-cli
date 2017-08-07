# Localise.biz CLI

[![PyPI version](https://img.shields.io/pypi/v/loco-cli.svg)](https://pypi.python.org/pypi/loco-cli)
[![Build](https://travis-ci.org/marten-cz/loco-cli.svg?branch=master)](https://travis-ci.org/marten-cz/loco-cli)

## Run

If you didn't used the script before, just run:

    python localise/localise.py config

and it will create configuration file in your home directory.

You will have to setup push part in the config as you need.

Call https://localise.biz/api#!/import/import

Then add synchronized files you need.

After that you can call `localise.py pull` and `localise.py push`.

## Notes

Merging can be done with msgfmt command line tool.
