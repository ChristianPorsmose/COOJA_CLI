import os
import random
import click

from cooja_cli.parts.interface.interface_configs import AbstractIdConfig, PositionConfig
from cooja_cli.parts.mote.mote import Mote
from cooja_cli.parts.motetype.motetype import MoteTypeSky, MoteTypeDisturber
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
@click.option("-mn","--makefile-name", default="Makefile", help="Makefile name")
@click.option("-id", "--mote-id", default=None, help="Mote ID for the new mote type")
@click.option("-cf", "--compile-flags", default="", help="Extra compile flags, comma-separated")
def add_mote_type(c_file, make_dir,makefile_name, mote_id,compile_flags):
    """Add a new mote type."""
    state = load_state()
    sim = Simulation.from_dict(state)
    mote_id = mote_id or (len(state.get("motetypes", [])) + 1)
    abs_path = os.path.abspath(c_file)
    build_dir = make_dir or os.path.dirname(abs_path)
    firmware_path = abs_path.replace(".c", ".sky")
    flags_list = [flag.strip() for flag in compile_flags.split(",") if flag.strip()]
    flags_str = " ".join(flags_list)
    sky_type = MoteTypeSky(
        id=mote_id,
        source=abs_path,
        firmware=firmware_path,
        command=f"make -f {makefile_name} -C {build_dir} TARGET=sky clean \
            \n make -f {makefile_name} -C {build_dir} -j$(CPUS) TARGET=sky {flags_str}",
        interfaces = [iface for iface in InterfaceType if iface != InterfaceType.ABSTRACT_ID]
    )
    sim.add_motetype(sky_type)
    state = sim.to_dict()
    save_state(state)
    click.echo(f"✅ Added mote type from {c_file} (Makefile dir: {build_dir})")


@motetype.command("add_disturbers")
@click.option("-n", "--number", default=1, type=int, help="number of disturbers")
def add_disturbers(number):
    """Add a new mote type."""
    state = load_state()
    sim = Simulation.from_dict(state)
    mote_id = len(state.get("motetypes", [])) + 1
    distuber_type = MoteTypeDisturber(
        id=mote_id,
    )
    for i in range(number):
        x=random.randint(0,100)
        y=random.randint(0,100)
        z=random.randint(0,100)
        position_config = PositionConfig(x,y,z)
        id_config = AbstractIdConfig(random.randint(0,5000))
        mote = Mote(configs=[position_config, id_config])
        distuber_type.add_mote(mote)
    sim.add_motetype(distuber_type)
    state = sim.to_dict()
    save_state(state)
    click.echo(f"✅ Added {number} disturbers")


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