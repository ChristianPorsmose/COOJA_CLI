from typing import List
from cooja_cli.parts.interface.interface_enum import InterfaceType
from cooja_cli.parts.mote.mote import Mote
from cooja_cli.parts.part import Part
import xml.etree.ElementTree as ET
from abc import abstractmethod

class MoteType(Part):
    def __init__(self, id: int):
        self.id = id
        self.description = ""
        self.motes: List[Mote] = []

    def add_mote(self, mote: Mote):
        self.motes.append(mote)

class MoteTypeSky(MoteType):
    def __init__(self, id: int, source: str, firmware: str, command: str, interfaces: List[InterfaceType] = []):
        super().__init__(id)
        self.source = source
        self.firmware = firmware
        self.command = command
        self.interfaces: List[InterfaceType] = interfaces

    def add_interface(self, mote_interface: InterfaceType):
        self.interfaces.append(mote_interface)

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
    def from_dict(cls, data: dict) -> "MoteTypeSky":
        mt = cls(
            id=data.get("id", 1),
            source=data.get("source", ""),
            firmware=data.get("firmware", ""),
            command=data.get("command", ""),
            interfaces=[InterfaceType(iface) for iface in data.get("interfaces", [])]
        )
        mt.description = data.get("description", "")
        mt.motes = [Mote.from_dict(m) for m in data.get("motes", [])]
        return mt


class MoteTypeDisturber(MoteType):
    def __init__(self, id: int):
        super().__init__(id)
        self.identifier = f"apptype{id}"

    def to_xml(self):
        mt_elem = ET.Element("motetype")
        mt_elem.text = "org.contikios.cooja.motes.DisturberMoteType"
        ET.SubElement(mt_elem, "identifier").text = self.identifier

        for mote in self.motes:
            mt_elem.append(mote.to_xml())
        return mt_elem

    def to_dict(self):
        return {
            "id": self.id,
            "identifier": self.identifier,
            "motes": [mote.to_dict() for mote in self.motes]
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MoteTypeDisturber":
        mt = cls(id=data.get("id", 1))
        mt.identifier = data.get("identifier", f"apptype{mt.id}")
        mt.motes = [Mote.from_dict(m) for m in data.get("motes", [])]
        return mt
