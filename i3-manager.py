import argparse, hjson, configparser, os
from pathlib import Path
from os import sep

# Takes the name of a config file, the applications configuration, and verbosity
# and produces the related xsession and i3 files
def generate(config_file, appconfig, verbosity):
    
    # Load the config file

    os.makedirs(appconfig['Main']['configs_dir'], exist_ok=True)
    with open(f"{appconfig['Main']['configs_dir']}{sep}{config_file}") as file:
        config = hjson.load(file)
        # Check if the config file contains a key named enable and if it's false
        if 'enable' in config and config['enable'] is False:
            print(f"Skipping generation of {config_file}, enable key set to false")
            return
        if verbosity >= 2:
            print(f"Generating files for config: {config_file}")

    try:

        # Determine filenames for xsessions file and i3 config file
        filename = config['filename'] if 'filename' in config else config['name']

        # Write i3 config file
        os.makedirs(appconfig['Main']['i3_config_output'], exist_ok=True)
        with open(f"{appconfig['Main']['i3_config_output']}{sep}{filename}", 'w') as file:

            file.write('#####      DO NOT MODIFY      #####\n')
            file.write('##### GENERATED BY I3-MANAGER #####\n')

            # Open every part listen in the config
            # Read each part file and write contents to final i3 config
            for part in config['parts']:
                with open(f"{appconfig['Main']['parts_dir']}{sep}{part}") as partfile:
                    file.write(partfile.read())
            
            if verbosity >= 3:
                print(f"Wrote i3 configuration file: {filename}")

        # Write xsessions file unless dont-generate-xsession=True
        if not config.get('dont-generate-xsession', False):
           
            xsession = configparser.ConfigParser()

            # Xsession files are ini-like
            xsession['Desktop Entry'] = {

                'Name': config['name'],

                'Comment': config.get('comment', ''),

                'Exec': f"i3 -c {os.path.abspath(appconfig['Main']['i3_config_output'])}{sep}{filename}",

                'Type': 'Application'

            }
           
           # Write the file
            os.makedirs(appconfig['Main']['desktop_files_output'], exist_ok=True)
            with open(f"{appconfig['Main']['desktop_files_output']}{sep}{filename}.xsession", 'w') as file:
                file.write('#####      DO NOT MODIFY      #####\n')
                file.write('##### GENERATED BY I3-MANAGER #####\n')
                xsession.write(file)

                if verbosity >= 3:
                    print(f"Wrote xsession file: {filename}")

    # KeyErrors might be raised if a config file is missing a key
    except KeyError as ke:
        print(f'Incorrect configuration file: \"{config_file}\"')
        print(ke)
        # Exit the application if fail-fast is enabled
        if appconfig['Main']['fail_fast']:
            print('Fail fast - Exiting!')
            exit(1)
    
    print(f"Generated config for {config_file}")

# Listing part files and config files works the same way
# This function prevents having to write the same code twice
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

    parser.add_argument('--verbosity', '-v', action='count', help='Defines verbosity of output (-v, -vv, -vvv)',
                    default=0)

    parser.add_argument('--config', '-c', type=str,
                    help='Use the specified config file')

    parser.add_argument('verb', type=str,
                    help='The action to perform (list-configs, list-parts, list-all, generate, diff)')

    args = parser.parse_args()

    if args.verbosity >= 3:
        print(f"Command line arguments: {args}")

    #
    # Config
    #

    appconfig = configparser.ConfigParser()

    # Use the supplied config file if provided
    config_file = args.config if args.config else 'config.ini'

    if not appconfig.read(config_file):
        raise ValueError(f'Could not load config file: \"{config_file}\"') # Config couldn't be found

    if args.verbosity >= 1:
        print(f'Read config file \"{config_file}\"')

    #
    # list-parts, list-configs, and list-all
    #

    if args.verb in ['list-parts', 'list-configs', 'list-all']:

        if args.verb in ['list-parts', 'list-all']:

            walk(appconfig['Main']['parts_dir'], 'part')
        
        if args.verb in ['list-configs', 'list-all']:

            walk(appconfig['Main']['configs_dir'], 'config')

    #
    # Generate
    #

    elif args.verb == 'generate':
        
        for _, _, configs in os.walk(appconfig['Main']['configs_dir']):
            for config in configs:
                generate(config, appconfig, args.verbosity)

    else:
        print(f'Unknown verb: \"{args.verb}\"')
        print('Did nothing')

if __name__ == "__main__":
    main()