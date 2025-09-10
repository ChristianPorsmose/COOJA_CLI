import xml.etree.ElementTree as ET

from cooja_cli.parts.plugin.plugin_config_base import PluginConfig
from cooja_cli.parts.plugin.plugin_configs import LogListenerConfig, ScriptRunnerConfig
from cooja_cli.parts.plugin.plugin_enum import PluginType
class Plugin:
    def __init__(self, plugin_type: PluginType, plugin_config : PluginConfig):
        self.plugin_type = plugin_type
        self.plugin_config = plugin_config

    def to_xml(self):
        plugin = ET.Element("plugin")
        plugin.text = self.plugin_type.value
        plugin.append(self.plugin_config.to_xml())
        return plugin
    
    def to_dict(self):
        return {
            "type": self.plugin_type.value,
            "config": self.plugin_config.to_dict()
        }
    
    # MAKE BETTER
    @classmethod
    def from_dict(cls, data: dict) -> "Plugin":
        ptype = PluginType(data["type"])
        if ptype == PluginType.SCRIPT_RUNNER:
            pconfig = ScriptRunnerConfig(
                file_source=data["config"]["file_source"],
                active=data["config"]["active"]
            )
        elif ptype == PluginType.LOG_LISTENER:
            pconfig = LogListenerConfig(
                active=data["config"]["active"]
            )
        else:
            raise ValueError(f"Unknown plugin type: {data['type']}")
        
        return cls(
            plugin_type=ptype,
            plugin_config=pconfig
        )
    