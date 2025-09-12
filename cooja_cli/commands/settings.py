import os
import click

from cooja_cli.utils import load_state, save_state

@click.group()
def settings():
    """Commands for simulations."""
    pass

@settings.command()
@click.option("-d","--dir", required=True, type=click.Path(), help="Path to Cooja directory")
def cooja_dir(dir):
    """Set the path to the Cooja installation for this project."""
    state = load_state(state_file="settings.json")
    state["cooja_dir"] = os.path.abspath(dir)
    save_state(state, state_file="settings.json")
    click.echo(f"✅ Cooja directory set to: {state['cooja_dir']}")

@settings.command()
@click.option("-d","--dir", required=True, type=click.Path(), help="Path to Cooja directory")
def output_dir(dir):
    """Set the path to the outputs for this project"""
    state = load_state(state_file="settings.json")
    state["output_dir"] = os.path.abspath(dir)
    os.makedirs(dir, exist_ok=True)
    save_state(state, state_file="settings.json")
    click.echo(f"✅ Cooja directory set to: {state['output_dir']}")

@settings.command("list")
def list_items():
    """lists all settings"""
    state = load_state("settings.json")
    click.echo("🔧 Current settings:")
    for key, value in state.items():
        click.echo(f"  {key}: {value}")