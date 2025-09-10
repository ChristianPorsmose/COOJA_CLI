from typing import List, Optional
from cooja_cli.parts.interface.interface_config_base import InterfaceConfig
from cooja_cli.parts.part import Part
import xml.etree.ElementTree as ET

class Mote(Part):
    def __init__(self, configs : Optional[List[InterfaceConfig]] = None):
        self.configs : List[InterfaceConfig] = configs or []

    def add_interface(self, mote_interface : InterfaceConfig):
        self.configs.append(mote_interface)

    def to_xml(self):
        mote_elem = ET.Element("mote")
        for interface in self.configs:
            mote_elem.append(interface.to_xml())
        return mote_elem
    
    def to_dict(self):
        return {
            "configs": [config.to_dict() for config in self.configs]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Mote":
        configs=[InterfaceConfig.from_dict(cfg) for cfg in data.get("configs", [])]
        return cls(
            configs=[InterfaceConfig.from_dict(cfg) for cfg in data.get("configs", [])]
        )