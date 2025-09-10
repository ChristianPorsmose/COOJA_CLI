import os
import click

from cooja_cli.parts.motetype.motetype import MoteType
from cooja_cli.parts.interface.interface_enum import InterfaceType
from cooja_cli.parts.simulation.simulation import Simulation
from cooja_cli.utils import load_state, save_state

@click.group()
def motetype():
    """Commands for mote types."""
    pass

@motetype.command("add")
@click.option("--project-dir", default="generated_sim", help="Project directory for the simulation")
@click.option("-c", "--c-file", required=True, help="Path to the C source file for the mote firmware")
@click.option("-m", "--make-dir", default=None, type=click.Path(), help="Directory containing the Makefile (defaults to C file dir)")
@click.option("-d", "--description", default=None, help="Description for the mote type")
@click.option("-id", "--mote-id", default=None, help="Mote ID for the new mote type")
def add_mote_type(project_dir, c_file, make_dir, description, mote_id):
    """Add a new mote type."""
    state = load_state(project_dir)
    sim = Simulation.from_dict(state)
    mote_id = mote_id or (len(state.get("motetypes", [])) + 1)
    description = description or os.path.basename(c_file)
    build_dir = make_dir or os.path.dirname(c_file)
    sky_type = MoteType(
        id=mote_id,
        description=f"Sky Mote Type from {description}",
        source=c_file,
        firmware=c_file.replace(".c", ".sky"),
        command=f"make -C {build_dir} TARGET=sky clean \n make -C {build_dir} -j$(CPUS) {os.path.basename(c_file).replace('.c', '.sky')} TARGET=sky",
        interfaces=list(InterfaceType)
    )
    sim.add_motetype(sky_type)
    state = sim.to_dict()
    save_state(state, project_dir)
    click.echo(f"✅ Added mote type from {c_file} (Makefile dir: {build_dir})")

@motetype.command("remove")
@click.option("--project-dir", default="generated_sim", help="Project directory for the simulation")
@click.option("-id", "--mote-id", required=True, type=int, help="Mote type ID to remove")
def remove_mote_type(project_dir, mote_id):
    """Remove a mote type by its ID."""
    state = load_state(project_dir)
    sim = Simulation.from_dict(state)
    original_count = len(sim.motetypes)
    sim.motetypes = [mt for mt in sim.motetypes if mt.id != mote_id]
    if len(sim.motetypes) == original_count:
        click.echo(f"No mote type found with ID {mote_id}.")
    else:
        save_state(sim.to_dict(), project_dir)
        click.echo(f"✅ Removed mote type with ID {mote_id}.")