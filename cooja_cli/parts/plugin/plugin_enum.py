from enum import Enum


class PluginType(Enum):
    SCRIPT_RUNNER = "org.contikios.cooja.plugins.ScriptRunner"
    LOG_LISTENER = "org.contikios.cooja.plugins.LogListener"

