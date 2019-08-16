# i3-manager
Enables you to manage multiple i3 configurations that share configuration code and generate related XSession files for session managers.

## Installation
- Clone this repository and place the folder in a suitable location, I recommend ~/.config
- By default the script looks for parts and configs within the same folder as the script, however this can be configured in config.ini
- Similarly i3 files are by default output to ~/.config/i3/configs and xsession files to /usr/share/xsessions
  - you will need to run the script with elevated permissions or change write access to /usr/share/xsessions
- I recommend making i3-manager (included bash file) executable anywhere so symlinking it may not be a bad idea

## Usage

> -h | Displays the help text  
> -v -vv -vvv | varying levels of verbosity  
> -c --config | specify an alternative config.ini  
> verb | Must be one of:  
> - a  
