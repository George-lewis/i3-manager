import argparse, hjson, configparser
from pathlib import Path
from os import sep

def main():

    config = configparser.ConfigParser()
    
    parser = argparse.ArgumentParser(description='Generate and manage i3 configuration files.')

    parser.add_argument('--verbose', '-v', action='count', help='Defines verbosity of output (-v, -vv, -vvv)',
                    default=0)

    parser.add_argument('--config', '-c', type=str,
                    help='Use the specified config file')

    parser.add_argument('verb', type=str,
                    help='The action to perform (list-configs, list-parts, generate)')

    args = parser.parse_args()

    if args.verbose >= 2:
        print(args)

    if args.config:
        config.read(args.config)
    else:
        config.read(f'{Path.home()}{sep}.config{sep}i3-manager{sep}config.ini')

    

if __name__ == "__main__":
    main()