import xml.etree.ElementTree as ET
import xml.dom.minidom as md
import os
import json
import subprocess
import click

from cooja_cli.parts.simulation.simulation import Simulation

STATE_FILE = "sim_state.json"

def save_state(state, project_dir):
    os.makedirs(project_dir, exist_ok=True)
    with open(os.path.join(project_dir, STATE_FILE), "w") as f:
        json.dump(state, f, indent=2)

def load_state(project_dir):
    state_path = os.path.join(project_dir, STATE_FILE)
    if not os.path.exists(state_path):
        raise click.ClickException(f"No simulation initialized in {project_dir}")
    with open(state_path) as f:
        return json.load(f)

def save(sim: Simulation, filename):
    rough_string = ET.tostring(sim.to_xml(), 'utf-8')
    reparsed = md.parseString(rough_string)
    with open(filename, 'w') as f:
        f.write(reparsed.toprettyxml(indent="  "))

def copy_log_file_to_output(log_file: str, output_file: str):
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(log_file, 'r') as src, open(output_file, 'w') as dst:
            dst.write(src.read())
        click.echo(f"✅ Log file copied to {output_file}")
    except Exception as e:
        click.echo(f"⚠ Failed to copy log file: {e}")
