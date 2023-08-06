# StellaNow CLI

StellaNow CLI is a command-line interface for interacting with the StellaNow services.

## Installation
To install StellaNow CLI, you can use pip:

    pip install -e .

This command installs the CLI in editable mode, which is convenient for development purposes.

## Usage
After installation, you can use the **'stellanow'** command in your terminal to interact with StellaNow services. Here is how to use some of the available commands:

### Configure
You can use the **'configure'** command to setup the necessary credentials and configurations for a specific profile. The profile will store a particular set of configurations.

Here is how to use the command:

    stellanow configure --profile YOUR_PROFILE_NAME

If no profile is specified, the configurations will be stored under the 'DEFAULT' profile.

### Environment Variables
The stellanow CLI can also read the following environment variables:

* **`STELLANOW_ACCESS_KEY`**: Your access key.
* **`STELLANOW_ACCESS_TOKEN`**: Your access token.


These environment variables take precedence over the settings from the command line options and your configuration file. The precedence order is: 
    
    Environment Variables -> Command Line Options -> Configuration File

### Development
StellaNow CLI is built using the Python Click library.

If you want to add a new command, follow these steps:

* Create a new Python file for your command in the **'commands'** directory.
* Define your command as a function, and decorate it with the **'@click.command()'** decorator.
* In **'cli.py'**, import your command function and add it to the main cli group using **'cli.add_command(your_command_function)'**.

Please note that StellaNow CLI follows the conventions of Python Click library.