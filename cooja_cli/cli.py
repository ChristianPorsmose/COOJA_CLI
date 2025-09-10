import os
import subprocess
import click

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

@cli.command()
@click.option("--project-dir", default="generated_sim", help="Project directory for the simulation")
@click.option("--build/--no-build", default=False, help="Build the simulation CSC file")
@click.option("--run/--no-run", default=True, help="Run the simulation using Cooja")
@click.option("-n", "--name", default="simulation.csc", help="Output CSC file name")
@click.option("-o", "--output-dir", required=True, help="Output directory for sim and logs")
def build_and_run(project_dir, build, run, name, output_dir):
    """Build and/or run the simulation."""
    state = load_state(project_dir)
    sim = Simulation.from_dict(state)

    output_dir = os.path.abspath(output_dir)

    # Ensure name ends with .csc
    if not name.lower().endswith(".csc"):
        name += ".csc"

    # If build=False, use a temporary file for the CSC
    if build:
        csc_path = os.path.join(output_dir, name)
        save(sim, csc_path)
        click.echo(f"✅ Simulation CSC file saved to {csc_path}")
    else:
        # Use a temporary file that will auto-delete
        temp_file = tempfile.NamedTemporaryFile(suffix=".csc", delete=False)
        csc_path = temp_file.name
        save(sim, csc_path)
        temp_file.close()  # make sure Cooja can open it
        click.echo(f"ℹ Temporary CSC file created at {csc_path} for running simulation")

    if run:
        cooja_dir = state.get("cooja_dir")
        if not cooja_dir:
            raise click.ClickException("Cooja directory not set. Run 'set-cooja-dir' first.")
        cooja_gradle = os.path.join(cooja_dir, "gradlew")
        args = f"--no-gui {csc_path}"
        try:
            subprocess.run([cooja_gradle, "run", f"--args={args}"],
                           check=True, cwd=cooja_dir,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            click.echo("✅ Simulation ran successfully!")
        except subprocess.CalledProcessError as e:
            click.echo(f"⚠ Simulation run failed: {e}")

        copy_log_file_to_output(
            os.path.join(cooja_dir, "COOJA.testlog"),
            os.path.join(output_dir, name.replace(".csc", ".log"))
        )

    # Clean up the temporary file if we didn’t build permanently
    if not build:
        os.remove(csc_path)
        click.echo(f"ℹ Temporary CSC file {csc_path} deleted")


@cli.command()
@click.option("--project-dir", default="generated_sim", help="Project directory for the simulation")
@click.option("--cooja-dir", required=True, type=click.Path(), help="Path to Cooja directory")
def set_cooja_dir(project_dir, cooja_dir):
    """Set the path to the Cooja installation for this project."""
    state = load_state(project_dir)
    state["cooja_dir"] = os.path.abspath(cooja_dir)
    save_state(state, project_dir)
    click.echo(f"✅ Cooja directory set to: {state['cooja_dir']}")

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