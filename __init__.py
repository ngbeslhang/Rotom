from .rotom import Bot

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Runs Rotom.')
    parser.add_argument('-c', '--config', type=str, help='Config file name (default: config.yml)')
    parser.add_argument('-d', '--debug', help='Enable debug mode', action='store_true')
    args = parser.parse_args()
    if args.config is None:
        args.config = 'config.yml'
    rotom = Bot(config=args.config, debug=args.debug)
    rotom.run()