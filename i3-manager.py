import argparse, hjson, configparser, os
from pathlib import Path
from os import sep

def walk(directory, files_name):

    print(f'{files_name.capitalize()} files:')

    count = 0
            
    for root, _, files in os.walk(directory):
        for file in files:
            count += 1
            print(f'{root}{sep}{file}')

    if count == 0:
        print(f"There's no {files_name} files")
    else:
        print(f"Found {count} {files_name} {'file' if count == 1 else 'files'}!")

def main():

    #
    # Argument parsing
    #

    parser = argparse.ArgumentParser(description='Generate and manage i3 configuration files.')

    parser.add_argument('--verbose', '-v', action='count', help='Defines verbosity of output (-v, -vv, -vvv)',
                    default=0)

    parser.add_argument('--config', '-c', type=str,
                    help='Use the specified config file')

    parser.add_argument('verb', type=str,
                    help='The action to perform (list-configs, list-parts, list-all, generate, diff)')

    args = parser.parse_args()

    if args.verbose >= 2:
        print(args)

    #
    # Config
    #

    config = configparser.ConfigParser()

    config_file = args.config if args.config else 'config.ini'

    if not config.read(config_file):
        raise ValueError(f'Could not load config file: \"{config_file}\"') # Config couldn't be found

    if args.verbose >= 1:
        print(f'Read config file \"{config_file}\"')

    #
    # list-parts, list-configs, and list-all
    #

    if args.verb in ['list-parts', 'list-configs', 'list-all']:

        if args.verb in ['list-parts', 'list-all']:

            walk(config['Main']['parts_dir'], 'part')
        
        if args.verb in ['list-configs', 'list-all']:

            walk(config['Main']['configs_dir'], 'config')

    #
    # Generate
    #

    elif args.verb == 'generate':
        pass


    else:
        print(f'Unknown verb: \"{args.verb}\"')
        print('Did nothing')

if __name__ == "__main__":
    main()