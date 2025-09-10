from cooja_cli.parts.part import Part

# this should be like InterfaceConfig base ? 
class PluginConfig(Part):
    def __init__(self):
        pass

    def to_xml(self):
        pass

    def to_dict(self):
        pass

    @classmethod
    def from_dict(cls, data):
        pass