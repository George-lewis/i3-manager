# i3-manager
i3-manager enables you to manage multiple i3 configurations that share common configuration code and generate related the XSession files for use by session managers.

## Background

i3 is a great and minimal tiling window manager with a fairly straightforward configuration scheme. However I don't always want to use the same configuration every time and i3's support of this is quite low. Often times I'd find that my different configurations would share most of their code and only differ in a few ways. In order to make that work I would have to manually copy and paste all the shared code every time I made an update to it. Which is what motivated me to create i3-manager. i3-manager will take parts of configuration files and combine them into multiple i3 configurations for you, in addition to this, it will also generate the correct XSession files used by many login/session managers to launch desktop environments.

## Installation
- Clone this repository and place the folder in a suitable location, I recommend ~/.config
- By default the script looks for parts and configs within the same folder as the script, however this can be configured in config.ini
- Similarly i3 files are by default output to ~/.config/i3/configs and xsession files to /usr/share/xsessions
  - you will need to run the script with elevated permissions or change write access to /usr/share/xsessions
- I recommend making i3-manager (included bash file) executable anywhere so symlinking it may not be a bad idea

## Usage

Part files:
- Part files are *parts* of i3 config and are combined by i3 manager to create i3 configurations

Conf files:
- Describes to i3-manager how to combine parts files into i3 configurations
	
	Structure:
		- name
			- This is the name used within the .desktop file
		- filename
			- Not necessary but allows you to have file names (e.g. the .desktop and i3 conf) that differ from the `name` variable
		- Comment
			- This comment gets put into the .desktop file
		- Parts
			- The most important section
			- Declares an array of part file names
				- These part files are combined linearly to produce the i3 configuration

Once you have parts and confs you can run `i3-manager generate` to generate the config files.
