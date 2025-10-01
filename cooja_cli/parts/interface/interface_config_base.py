from cooja_cli.parts.interface.interface_enum import InterfaceType
from cooja_cli.parts.part import Part


class InterfaceConfig(Part):
    def __init__(self, iface_type: InterfaceType):
        self.iface_type = iface_type

    def to_xml(self):
        pass

    def to_dict(self):
        pass

    # OPTIMIZE THIS LATER USING A REGISTRY OR SOMETHING
    @classmethod
    def from_dict(cls, data: dict) -> "InterfaceConfig":
        iface_type = data.get("type")

        # import subclasses lazily, only when this method is called
        from cooja_cli.parts.interface.interface_configs import (
            PositionConfig,
            MoteIDConfig,
            IPAddressConfig,
            MSPClockConfig,
            MSPRadioConfig,
            MSPSerialConfig,
            AbstractIdConfig
        )

        if iface_type == InterfaceType.POSITION.value:
            return PositionConfig.from_dict(data)
        elif iface_type == InterfaceType.MSP_MOTE_ID.value:
            return MoteIDConfig.from_dict(data)
        elif iface_type == InterfaceType.IPADDRESS.value:
            return IPAddressConfig.from_dict(data)
        elif iface_type == InterfaceType.MSP_CLOCK.value:
            return MSPClockConfig.from_dict(data)
        elif iface_type == InterfaceType.MSP_RADIO.value:
            return MSPRadioConfig.from_dict(data)
        elif iface_type == InterfaceType.MSP_SERIAL.value:
            return MSPSerialConfig.from_dict(data)
        elif iface_type == InterfaceType.ABSTRACT_ID.value:
            return AbstractIdConfig.from_dict(data)
        else:
            raise ValueError(f"Unknown interface type: {iface_type}")