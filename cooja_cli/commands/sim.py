import os
import subprocess
import tempfile
import traceback
import click
from cooja_cli.parts.interface.interface_configs import MoteIDConfig, PositionConfig
from cooja_cli.parts.simulation.simulation import Simulation
from cooja_cli.parts.interface.interface_enum import InterfaceType
from cooja_cli.parts.plugin.plugin_enum import PluginType
from cooja_cli.parts.plugin.plugin_configs import LogListenerConfig, ScriptRunnerConfig
from cooja_cli.utils import copy_log_file_to_output, load_state, save, save_state

@click.group()
def sim():
    """Commands for simulations."""
    pass


@sim.command("init")
def init():
    """Initialize a new simulation project."""
    state = Simulation().to_dict()
    save_state(state)
    click.echo(f"✅ Initialized new simulation")

@sim.command("list")
@click.option("--detailed/--no-detailed", default=False, help="Show detailed information")
def list_items(detailed):
    """List all mote types, motes, and plugins in the simulation."""
    state = load_state()
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



@sim.command()
@click.option("-n", "--name", default="simulation.csc", help="Output CSC file name")
def build(name:str):
    """Build sim file"""
    settings = load_state("settings.json")
    output_dir = settings.get("output_dir")
    state = load_state()
    sim = Simulation.from_dict(state)
    if not name.lower().endswith(".csc"):
        name += ".csc"
    csc_path = os.path.join(output_dir, name)
    save(sim, csc_path)
    click.echo(f"✅ Simulation CSC file saved to {csc_path}")

@sim.command()
@click.option("-n", "--name", default="simulation.log", help="Output log file name")
def run(name:str):
    if not name.lower().endswith(".log"):
        name += ".log"
    settings = load_state("settings.json")
    output_dir = settings.get("output_dir",".")
    state = load_state()
    sim = Simulation.from_dict(state)
    temp_file = tempfile.NamedTemporaryFile(suffix=".csc", delete=False)
    csc_path = temp_file.name
    save(sim, csc_path)
    temp_file.close()
    click.echo(f"ℹ Temporary CSC file created at {csc_path} for running simulation")
    settings = load_state(state_file="settings.json")
    cooja_dir = settings.get("cooja_dir")
    if not cooja_dir:
        raise click.ClickException("Cooja directory not set. Run 'set-cooja-dir' first.")
    cooja_gradle = os.path.join(cooja_dir, "gradlew")
    args = f"--no-gui {csc_path}"
    try:
        subprocess.run([cooja_gradle, "run", f"--args={args}"],
                       check=True, cwd=cooja_dir,
                        text=True,
                        capture_output=True)
        click.echo("✅ Simulation ran successfully!")
    except subprocess.CalledProcessError as e:
        click.secho("⚠ Simulation run failed!", fg="red", bold=True)
        click.secho(f"Exit code: {e.returncode}", fg="red", bold=True)
        full_output = (e.stdout or "") + (e.stderr or "")
        if "ERROR [main] [Cooja.java:1215] - Failed tests:" in full_output:
            click.secho(
                "⚠ Simulation run failed — check script file for errors", fg="red", bold=True
            )
        click.secho(
            "⚠ Generated log file will be from the previously successful run", fg="blue", bold=True
        )
    copy_log_file_to_output(
        os.path.join(cooja_dir, "COOJA.testlog"),
        os.path.join(output_dir, name)
    )
    os.remove(csc_path)
    click.echo(f"ℹ Temporary CSC file {csc_path} deleted")
