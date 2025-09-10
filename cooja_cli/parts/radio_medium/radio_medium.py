
from cooja_cli.parts.part import Part
import xml.etree.ElementTree as ET

class RadioMedium(Part):
    def __init__(
            self,
            transmitting_range=50.0, 
            interference_range=100,
            success_ratio_tx=1,
            success_ratio_rx=1
            ):
        self.transmitting_range : float = transmitting_range
        self.interference_range : float = interference_range
        self.success_ratio_tx :float = success_ratio_tx
        self.success_ratio_rx :float= success_ratio_rx

    def to_xml(self):
        radio_medium = ET.Element("radiomedium")
        radio_medium.text = "org.contikios.cooja.radiomediums.UDGM"
        ET.SubElement(radio_medium, "transmitting_range").text = str(self.transmitting_range)
        ET.SubElement(radio_medium, "interference_range").text = str(self.interference_range)
        ET.SubElement(radio_medium, "success_ratio_tx").text = str(self.success_ratio_tx)
        ET.SubElement(radio_medium, "success_ratio_rx").text = str(self.success_ratio_rx)
        return radio_medium
    
    def to_dict(self):
        return {
            "transmitting_range": self.transmitting_range,
            "interference_range": self.interference_range,
            "success_ratio_tx": self.success_ratio_tx,
            "success_ratio_rx": self.success_ratio_rx
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "RadioMedium":
        return cls(
            transmitting_range=data.get("transmitting_range", 50.0),
            interference_range=data.get("interference_range", 100),
            success_ratio_tx=data.get("success_ratio_tx", 1),
            success_ratio_rx=data.get("success_ratio_rx", 1)
        )