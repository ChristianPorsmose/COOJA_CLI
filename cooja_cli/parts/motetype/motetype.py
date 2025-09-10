# SHOULD I PUT MOTEINTERFACE IN MOTES 
# AND THEN LET MOTETYPE FETCH ALL REQUIRED FROM MOTES??
# I DONT THINK SO AS OF NOW, I THINK THEY AUTCONFIGURE IF NOT SET?? 
from typing import List

from cooja_cli.parts.interface.interface_enum import InterfaceType
from cooja_cli.parts.mote.mote import Mote
from cooja_cli.parts.part import Part
import xml.etree.ElementTree as ET

class MoteType(Part):
    def __init__(self, id, description, source, firmware, command, interfaces : List[InterfaceType] = []):
        self.id = id
        self.description = description
        self.source = source
        self.firmware = firmware
        self.command = command
        self.motes : List[Mote] = []
        self.interfaces : List[InterfaceType] = interfaces

    def add_interface(self, mote_interface):
        self.interfaces.append(mote_interface)

    def add_mote(self, mote):
        self.motes.append(mote)

    def to_xml(self):
        mt_elem = ET.Element("motetype")
        mt_elem.text = "org.contikios.cooja.mspmote.SkyMoteType"
        ET.SubElement(mt_elem, "description").text = self.description
        ET.SubElement(mt_elem, "source").text = self.source
        ET.SubElement(mt_elem, "firmware").text = self.firmware
        ET.SubElement(mt_elem, "commands").text = self.command

        for interface in self.interfaces:
            ET.SubElement(mt_elem, "moteinterface").text = interface.value

        for mote in self.motes:
            mt_elem.append(mote.to_xml())
        return mt_elem
    
    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "source": self.source,
            "firmware": self.firmware,
            "command": self.command,
            "interfaces": [iface.value for iface in self.interfaces],
            "motes": [mote.to_dict() for mote in self.motes]
        }
    
    @classmethod
    def from_dict(self, data: dict) -> "MoteType":
        mt = MoteType(
            id=data.get("id", 1),
            description=data.get("description", ""),
            source=data.get("source", ""),
            firmware=data.get("firmware", ""),
            command=data.get("command", ""),
            interfaces=[InterfaceType(iface) for iface in data.get("interfaces", [])]
        )
        mt.motes = [Mote.from_dict(m) for m in data.get("motes", [])]
        return mt