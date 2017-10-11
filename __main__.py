from rotom import Bot
import argparse

parser = argparse.ArgumentParser(description='Runs Rotom.')
parser.add_argument('-c', '--config', type=str, help='Config file name (default: config.yml)')
parser.add_argument('-d', '--debug', help='Enable debug mode', action='store_false')
parser.add_argument('-s', '--setup', help='Set up the bot', action='store_false')
args = parser.parse_args()

rotom = Bot(config=args.config, debug=args.debug)
rotom.run()
