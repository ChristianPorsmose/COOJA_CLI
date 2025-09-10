import click

from cooja_cli.parts.interface.interface_configs import MoteIDConfig, PositionConfig
from cooja_cli.parts.simulation.simulation import Simulation
from cooja_cli.parts.mote.mote import Mote
from cooja_cli.parts.interface.interface_enum import InterfaceType
from cooja_cli.utils import load_state, save_state

@click.group()
def mote():
    """Commands for individual motes."""
    pass

@mote.command("add")
@click.option("--project-dir", default="generated_sim", help="Project directory for the simulation")
@click.option("-mtid", "--mote-type-id", required=True, type=int, help="Mote type ID to which the mote will be added")
@click.option("-x", "--x", default=0, type=int, help="X position of the mote")
@click.option("-y", "--y", default=0, type=int, help="Y position of the mote")
@click.option("-z", "--z", default=0, type=int, help="Z position of the mote")
@click.option("-id", "--mote-id", default=0, type=int, help="Mote ID for the new mote")
def add_mote(project_dir, mote_type_id, x, y, z, mote_id):
    """Add a new mote instance."""
    state = load_state(project_dir)
    sim = Simulation.from_dict(state)
    mote_type = next((mt for mt in sim.motetypes if mt.id == mote_type_id), None)
    if not mote_type:
        raise click.ClickException(f"Mote type ID {mote_type_id} not found.")
    position_config = PositionConfig(x=x, y=y, z=z)
    mote_id = mote_id or (len(mote_type.motes) + 1)
    id_config = MoteIDConfig(mote_id)
    mote = Mote(configs=[position_config, id_config])
    mote_type.add_mote(mote)
    save_state(sim.to_dict(), project_dir)
    click.echo(f"✅ Added mote at position ({x}, {y}, {z}) to mote type ID {mote_type_id}")

@mote.command("remove")
@click.option("--project-dir", default="generated_sim", help="Project directory for the simulation")
@click.option("-mtid", "--mote-type-id", required=True, type=int, help="Mote type ID from which to remove the mote")
@click.option("-id", "--mote-id", required=True, type=int, help="Mote ID to remove")
def remove_mote(project_dir, mote_type_id, mote_id):
    """Remove a mote by its ID from a specific mote type."""
    state = load_state(project_dir)
    sim = Simulation.from_dict(state)
    mote_type = next((mt for mt in sim.motetypes if mt.id == mote_type_id), None)
    if not mote_type:
        raise click.ClickException(f"Mote type ID {mote_type_id} not found.")
    original_count = len(mote_type.motes)
    mote_type.motes = [m for m in mote_type.motes if not any(cfg.iface_type == InterfaceType.MSP_MOTE_ID and cfg.mote_id == mote_id for cfg in m.configs)]
    if len(mote_type.motes) == original_count:
        raise click.ClickException(f"Mote ID {mote_id} not found in mote type ID {mote_type_id}.")
    save_state(sim.to_dict(), project_dir)
    click.echo(f"✅ Removed mote ID {mote_id} from mote type ID {mote_type_id}")


