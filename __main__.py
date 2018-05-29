# -*- coding: utf-8 -*-
import argparse

from sys import exit
from core import Bot,  __version__

parser = argparse.ArgumentParser(description='Runs Rotom.')

parser.add_argument('-c', '--config', type=str, help='Config file name (default: config.yml)')
parser.add_argument('-d', '--debug', help='Enable debug mode', action='store_false')
parser.add_argument('-i', 
                    '--ignore-locale', 
                    help='Ignore config and system\'s locale', 
                    action='store_false')
parser.add_argument('-s', '--setup', help='Set up the bot', action='store_false')
parser.add_argument('-v', '--version', help='Get bot\'s current version', action='store_true')
                    
args = parser.parse_args()

if args.version:
    print(f"Current version of Rotom is: {__version__}")
    exit(0)
if args.config == None:
    args.config = 'config.yml'
# if args.setup:

rotom = Bot(config=args.config, debug=args.debug)
rotom.run()