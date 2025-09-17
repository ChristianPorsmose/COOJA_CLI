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
@click.option("-c", "--c-file", required=True, help="Path to the C source file for the mote firmware")
@click.option("-m", "--make-dir", default=None, help="Makefile path")
@click.option("-mn","--makefile-name", default=None, help="Makefile name")
@click.option("-d", "--description", default=None, help="Description for the mote type")
@click.option("-id", "--mote-id", default=None, help="Mote ID for the new mote type")
@click.option("-cf", "--compile-flags", default="", help="Extra compile flags")
def add_mote_type(c_file, make_dir,makefile_name, description, mote_id,compile_flags):
    """Add a new mote type."""
    state = load_state()
    sim = Simulation.from_dict(state)
    mote_id = mote_id or (len(state.get("motetypes", [])) + 1)
    description = description or os.path.basename(c_file)
    abs_path = os.path.abspath(c_file)
    build_dir = make_dir or os.path.dirname(abs_path)
    firmware_path = abs_path.replace(".c", ".sky")
    flags_str = f'CFLAGS="{compile_flags}"' if compile_flags else ""
    sky_type = MoteType(
        id=mote_id,
        description=f"Sky Mote Type from {description}",
        source=abs_path,
        firmware=firmware_path,
        command=f"make -f {makefile_name} -C {build_dir} TARGET=sky clean \
            \n make -f {makefile_name} -C {build_dir} -j$(CPUS) TARGET=sky {flags_str}",
        interfaces=list(InterfaceType)
    )
    sim.add_motetype(sky_type)
    state = sim.to_dict()
    save_state(state)
    click.echo(f"✅ Added mote type from {c_file} (Makefile dir: {build_dir})")

@motetype.command("remove")
@click.option("-id", "--mote-id", required=True, type=int, help="Mote type ID to remove")
def remove_mote_type(mote_id):
    """Remove a mote type by its ID."""
    state = load_state()
    sim = Simulation.from_dict(state)
    original_count = len(sim.motetypes)
    sim.motetypes = [mt for mt in sim.motetypes if mt.id != mote_id]
    if len(sim.motetypes) == original_count:
        click.echo(f"No mote type found with ID {mote_id}.")
    else:
        save_state(sim.to_dict())
        click.echo(f"✅ Removed mote type with ID {mote_id}.")