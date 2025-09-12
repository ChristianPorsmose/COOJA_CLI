import os
import click
from cooja_cli.parts.plugin.plugin import Plugin
from cooja_cli.parts.plugin.plugin_enum import PluginType
from cooja_cli.parts.plugin.plugin_configs import LogListenerConfig, ScriptRunnerConfig
from cooja_cli.parts.simulation.simulation import Simulation
from cooja_cli.utils import load_state, save_state

@click.group()
def plugin():
    """Commands for plugins."""
    pass

@plugin.command("add")
@click.option("-c", "--config", required=True, help="Configuration for the plugin (e.g., script file path)")
def add_plugin(config):
    """Add a new plugin."""
    state = load_state()
    sim = Simulation.from_dict(state)
    abs_path = os.path.abspath(config)
    script_runner_plugin = Plugin(PluginType.SCRIPT_RUNNER, ScriptRunnerConfig(file_source=abs_path, active=True))
    log_listener_plugin = Plugin(PluginType.LOG_LISTENER, LogListenerConfig(active=True))
    sim.add_plugin(script_runner_plugin)
    sim.add_plugin(log_listener_plugin)
    save_state(sim.to_dict())
    click.echo(f"✅ Added plugins to the simulation")

@plugin.command("remove")
def remove_plugin():
    """Remove all plugins."""
    state = load_state()
    sim = Simulation.from_dict(state)
    sim.plugins.clear()
    save_state(sim.to_dict())
    click.echo(f"✅ Removed all plugins from the simulation")