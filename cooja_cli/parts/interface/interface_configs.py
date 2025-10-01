import xml.etree.ElementTree as ET


from cooja_cli.parts.interface.interface_config_base import InterfaceConfig
from cooja_cli.parts.interface.interface_enum import InterfaceType

class PositionConfig(InterfaceConfig):
    def __init__(self, x=0, y=0, z=0):
        super().__init__(InterfaceType.POSITION)
        self.x, self.y, self.z = x, y, z

    def to_xml(self):
        elem = ET.Element("interface_config")
        elem.text = self.iface_type.value
        pos_elem = ET.SubElement(elem, "pos")
        pos_elem.set("x", str(self.x))
        pos_elem.set("y", str(self.y))
        pos_elem.set("z", str(self.z))
        return elem
    
    def to_dict(self):
        return {
            "type": self.iface_type.value,
            "x": self.x,
            "y": self.y,
            "z": self.z
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "PositionConfig":
        return cls(
            x=data.get("x", 0),
            y=data.get("y", 0),
            z=data.get("z", 0)
        )


class MoteIDConfig(InterfaceConfig):
    def __init__(self, mote_id: int):
        super().__init__(InterfaceType.MSP_MOTE_ID)
        self.mote_id = mote_id

    def to_xml(self):
        elem = ET.Element("interface_config")
        elem.text = self.iface_type.value
        ET.SubElement(elem, "id").text = str(self.mote_id)
        return elem
    
    def to_dict(self):
        return {
            "type": self.iface_type.value,
            "mote_id": self.mote_id
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "MoteIDConfig":
        return cls(
            mote_id=data.get("mote_id", 1)
        )


class IPAddressConfig(InterfaceConfig):
    def __init__(self, address: str):
        super().__init__(InterfaceType.IPADDRESS)
        self.address = address

    def to_xml(self):
        elem = ET.Element("interface_config")
        elem.text = self.iface_type.value
        ET.SubElement(elem, "address").text = self.address
        return elem
    
    def to_dict(self):
        return {
            "type": self.iface_type.value,
            "address": self.address
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "IPAddressConfig":
        return cls(
            address=data.get("address", "fe80::1")
        )


class MSPClockConfig(InterfaceConfig):
    def __init__(self):
        super().__init__(InterfaceType.MSP_CLOCK)

    def to_xml(self):
        elem = ET.Element("interface_config")
        elem.text = self.iface_type.value
        return elem
    
    def to_dict(self):
        return {
            "type": self.iface_type.value
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "MSPClockConfig":
        return cls()


class MSPRadioConfig(InterfaceConfig):
    def __init__(self):
        super().__init__(InterfaceType.MSP_RADIO)

    def to_xml(self):
        elem = ET.Element("interface_config")
        elem.text = self.iface_type.value
        return elem
    
    def to_dict(self):
        return {
            "type": self.iface_type.value
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "MSPRadioConfig":
        return cls()


class MSPSerialConfig(InterfaceConfig):
    def __init__(self):
        super().__init__(InterfaceType.MSP_SERIAL)

    def to_xml(self):
        elem = ET.Element("interface_config")
        elem.text = self.iface_type.value
        return elem
    
    def to_dict(self):
        return {
            "type": self.iface_type.value
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "MSPSerialConfig":
        return cls()


class AbstractIdConfig(InterfaceConfig):
    def __init__(self, mote_id: int):
        super().__init__(InterfaceType.ABSTRACT_ID)
        self.mote_id = mote_id

    def to_xml(self):
        elem = ET.Element("interface_config")
        elem.text = self.iface_type.value
        ET.SubElement(elem, "id").text = str(self.mote_id)
        return elem
    
    def to_dict(self):
        return {
            "type": self.iface_type.value,
            "abstract_id": self.mote_id
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "MoteIDConfig":
        return cls(
            mote_id=data.get("abstract_id", 1)
        )