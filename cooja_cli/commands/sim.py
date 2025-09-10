import click
from cooja_cli.parts.interface.interface_configs import MoteIDConfig, PositionConfig
from cooja_cli.parts.simulation.simulation import Simulation
from cooja_cli.parts.interface.interface_enum import InterfaceType
from cooja_cli.parts.plugin.plugin_enum import PluginType
from cooja_cli.parts.plugin.plugin_configs import LogListenerConfig, ScriptRunnerConfig
from cooja_cli.utils import load_state, save_state

@click.group()
def sim():
    """Commands for simulations."""
    pass


@sim.command("init")
@click.option("--project-dir", default="generated_sim", help="Project directory for the simulation")
def init(project_dir):
    """Initialize a new simulation project."""
    state = Simulation().to_dict()
    save_state(state, project_dir)
    click.echo(f"✅ Initialized new simulation in {project_dir}")

@sim.command("list")
@click.option("--project-dir", default="generated_sim", help="Project directory for the simulation")
@click.option("--detailed/--no-detailed", default=False, help="Show detailed information")
def list_items(project_dir, detailed):
    """List all mote types, motes, and plugins in the simulation."""
    state = load_state(project_dir)
    sim = Simulation.from_dict(state)

    click.echo("Mote Types:")
    for mt in sim.motetypes:
        click.echo(f"ID: {mt.id}, Description: {mt.description}, Source: {mt.source}")
        for idx, mote in enumerate(mt.motes, start=1):
            pos : PositionConfig = next((cfg for cfg in mote.configs if cfg.iface_type == InterfaceType.POSITION), None)
            mid : MoteIDConfig = next((cfg for cfg in mote.configs if cfg.iface_type == InterfaceType.MSP_MOTE_ID), None)
            pos_str = f"Position: ({pos.x}, {pos.y}, {pos.z})" if pos else "Position: N/A"
            id_str = f"Mote ID: {mid.mote_id}" if mid else "Mote ID: N/A"
            click.echo(f"Mote {idx}: {pos_str}, {id_str}")

    click.echo("\nPlugins:")
    for plugin in sim.plugins:
        click.echo(f" - {plugin.plugin_type}, Config: {plugin.plugin_type.value}")
        if detailed:
            if plugin.plugin_type == PluginType.SCRIPT_RUNNER:
                config: ScriptRunnerConfig = plugin.plugin_config
                click.echo(f"   ScriptRunner - File: {config}, Active: {config.active}")
            elif plugin.plugin_type == PluginType.LOG_LISTENER:
                config: LogListenerConfig = plugin.plugin_config
                click.echo(f"   LogListener - Active: {config.active}")
