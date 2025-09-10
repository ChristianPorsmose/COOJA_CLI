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
@click.option("--project-dir", default="generated_sim", help="Project directory for the simulation")
@click.option("-c", "--config", required=True, help="Configuration for the plugin (e.g., script file path)")
def add_plugin(project_dir, config):
    """Add a new plugin."""
    state = load_state(project_dir)
    sim = Simulation.from_dict(state)
    script_runner_plugin = Plugin(PluginType.SCRIPT_RUNNER, ScriptRunnerConfig(file_source=config, active=True))
    log_listener_plugin = Plugin(PluginType.LOG_LISTENER, LogListenerConfig(active=True))
    sim.add_plugin(script_runner_plugin)
    sim.add_plugin(log_listener_plugin)
    save_state(sim.to_dict(), project_dir)
    click.echo(f"✅ Added plugins to the simulation")