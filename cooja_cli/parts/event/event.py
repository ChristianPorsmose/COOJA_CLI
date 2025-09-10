from cooja_cli.parts.part import Part
import xml.etree.ElementTree as ET


class Event(Part):
    def __init__(self, log_output=40000):
        self.log_output = log_output

    def to_xml(self):
        events = ET.Element("events")
        ET.SubElement(events, "logoutput").text = str(self.log_output)
        return events
    
    def to_dict(self):
        return {
            "log_output": self.log_output
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Event":
        return cls(
            log_output=data.get("log_output", 40000)
        )