import os
import subprocess
import click

from cooja_cli.commands.settings import settings
from cooja_cli.parts.simulation.simulation import Simulation
from cooja_cli.commands.mote import mote
from cooja_cli.commands.plugin import plugin
from cooja_cli.commands.sim import sim
from cooja_cli.parts.plugin.plugin_enum import PluginType
from cooja_cli.utils import copy_log_file_to_output, load_state, save, save_state
from cooja_cli.commands.motetype import motetype

@click.group()
def cli():
    """Cooja Simulation Builder CLI."""

import tempfile




cli.add_command(settings)
cli.add_command(motetype)
cli.add_command(mote)
cli.add_command(plugin)
cli.add_command(sim)

if __name__ == "__main__":
    cli()

# TO ADD: remove-plugin, list-plugins
# TO ADD: configure-mote (change position, id, etc), configure-plugin (e.g., change script file)
# TO ADD: set-radio-medium (e.g., UDGM, etc), set-simulation-params (e.g., motedelay_us, title, etc)
# TO ADD: add other interfaces (e.g., IPAddressConfig, etc)
# TO ADD: add other plugins (e.g., LogListenerConfig, etc)
# TO ADD: validation (e.g., check if Cooja dir is valid, check if C file exists, etc)
# TO ADD: better error handling and user feedback
# TO ADD: simualtion events -> crash, etc

# create group for simulation commands
# create a list all motes, mote types, and plugins in the simulation


# all commands should have a print method


# fix bug where cooja-dir is not saved properly after adding a mote type or mote