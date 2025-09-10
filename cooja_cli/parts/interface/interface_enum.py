from enum import Enum


class InterfaceType(Enum):
    POSITION = "org.contikios.cooja.interfaces.Position"
    IPADDRESS = "org.contikios.cooja.interfaces.IPAddress"
    MOTE_RELATIONS = "org.contikios.cooja.interfaces.Mote2MoteRelations"
    ATTRIBUTES = "org.contikios.cooja.interfaces.MoteAttributes"
    MSP_CLOCK = "org.contikios.cooja.mspmote.interfaces.MspClock"
    MSP_MOTE_ID = "org.contikios.cooja.mspmote.interfaces.MspMoteID"
    SKY_BUTTON = "org.contikios.cooja.mspmote.interfaces.SkyButton"
    SKY_FLASH = "org.contikios.cooja.mspmote.interfaces.SkyFlash"
    SKY_FS = "org.contikios.cooja.mspmote.interfaces.SkyCoffeeFilesystem"
    MSP_RADIO = "org.contikios.cooja.mspmote.interfaces.Msp802154Radio"
    MSP_SERIAL = "org.contikios.cooja.mspmote.interfaces.MspSerial"
    MSP_LED = "org.contikios.cooja.mspmote.interfaces.MspLED"
    MSP_DEBUG = "org.contikios.cooja.mspmote.interfaces.MspDebugOutput"
    SKY_TEMP = "org.contikios.cooja.mspmote.interfaces.SkyTemperature"