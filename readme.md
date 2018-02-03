# Localise.biz CLI

[![PyPI version](https://img.shields.io/pypi/v/loco-cli.svg)](https://pypi.python.org/pypi/loco-cli)
[![PyPI downloads](https://img.shields.io/pypi/d/loco-cli.svg)](https://pypi.python.org/pypi/loco-cli)
[![Build](https://travis-ci.org/marten-cz/loco-cli.svg?branch=master)](https://travis-ci.org/marten-cz/loco-cli)
[![Analytics](https://ga-beacon.appspot.com/UA-24215296-4/marten-cz/loco-cli/)](https://github.com/igrigorik/ga-beacon)

## Run the cli command

### Requirements

This package need python to be installed. We support Python2 and Python3 as well.

### Install

To instal you can use the repository or install the package from PyPI.

    pip install loco-cli

To use the cli command, just type `loco-cli`. You need to have the python path in your PATH environment variable.
When you use the command for first time, you will need to create configuration file. Just run
`loco-cli -p <project name> config`. You can specify the path to config file with `-c <path>`.

You will have to setup push and pull config section as you need. See https://localise.biz/api#!/import/import for
supported variables.

Then add path to synchronized files as you need.

After that you can call `localise.py pull` and `localise.py push`.

## Notes

Merging can be done with msgfmt command line tool.
