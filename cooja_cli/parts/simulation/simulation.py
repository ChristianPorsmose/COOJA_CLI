from cooja_cli.parts.event.event import Event
from typing import List
import xml.etree.ElementTree as ET

from cooja_cli.parts.motetype.motetype import MoteType, MoteTypeDisturber, MoteTypeSky
from cooja_cli.parts.part import Part
from cooja_cli.parts.plugin.plugin import Plugin
from cooja_cli.parts.radio_medium.radio_medium import RadioMedium

class Simulation(Part):
    def __init__(self,motedelay_us=100000, title="Simulation"):
        self.title = title
        self.motetypes : List[MoteType] = []
        self.motedelay_us = motedelay_us
        self.plugins : List[Plugin] = []
        self.radio_medium = RadioMedium()
        self.event = Event()

    def set_radio_medium(self,radio_medium : RadioMedium):
        self.radio_medium = radio_medium

    def add_plugin(self, plugin):
        self.plugins.append(plugin)

    def add_motetype(self, motetype):
        self.motetypes.append(motetype)

    def to_xml(self):
        sim_elem = ET.Element("simconf")
        sim_elem.set("version", "2022112801")

        simulation = ET.SubElement(sim_elem, "simulation")
        ET.SubElement(simulation, "title").text = self.title
        ET.SubElement(simulation, "randomseed").text = "generated"
        ET.SubElement(simulation, "motedelay_us").text = str(self.motedelay_us)
        simulation.append(self.radio_medium.to_xml())
        simulation.append(self.event.to_xml())

        for plugin in self.plugins:
            sim_elem.append(plugin.to_xml())

        for mt in self.motetypes:
            simulation.append(mt.to_xml())

        return sim_elem

    def to_dict(self):
        return {
            "title": self.title,
            "motedelay_us": self.motedelay_us,
            "radio_medium": self.radio_medium.to_dict(),
            "event": self.event.to_dict(),
            "plugins": [plugin.to_dict() for plugin in self.plugins],
            "motetypes": [mt.to_dict() for mt in self.motetypes]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Simulation":
        if not data:
            return None
        sim = cls(
            motedelay_us=data.get("motedelay_us", 100000),
            title=data.get("title", "Simulation"),
        )
        # reconstruct subcomponents
        sim.radio_medium = RadioMedium.from_dict(data.get("radio_medium"))
        sim.event = Event.from_dict(data.get("event"))

        sim.plugins = [Plugin.from_dict(p) for p in data.get("plugins", [])]
        for mt_data in data.get("motetypes", []):
            if "source" in mt_data:  # Sky mote has source/firmware/command
                sim.motetypes.append(MoteTypeSky.from_dict(mt_data))
            elif "identifier" in mt_data:  # Disturber has identifier
                sim.motetypes.append(MoteTypeDisturber.from_dict(mt_data))

        return sim
