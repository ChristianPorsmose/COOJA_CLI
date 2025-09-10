from cooja_cli.parts.plugin.plugin_config_base import PluginConfig
import xml.etree.ElementTree as ET

class LogListenerConfig(PluginConfig):
    def __init__(self, active : bool):
        self.active = active
    
    def to_xml(self):
        plugin_config = ET.Element("plugin_config")
        ET.SubElement(plugin_config, "active").text = str(self.active).lower()
        return plugin_config
    
    def to_dict(self):
        return {
            "active": self.active
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "LogListenerConfig":
        return cls(
            active=data.get("active", True)
        )

class ScriptRunnerConfig(PluginConfig):
    def __init__(self, file_source, active : bool):
        self.file_source = file_source
        self.active = active
    
    def to_xml(self):
        plugin_config = ET.Element("plugin_config")
        ET.SubElement(plugin_config, "scriptfile").text = self.file_source
        ET.SubElement(plugin_config, "active").text = str(self.active).lower()
        return plugin_config
    
    def to_dict(self):
        return {
            "file_source": self.file_source,
            "active": self.active
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ScriptRunnerConfig":
        return cls(
            file_source=data.get("file_source", ""),
            active=data.get("active", True)
        )
