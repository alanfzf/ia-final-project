import time
import binascii
from pn532pi import Pn532, pn532
from pn532pi import Pn532I2c

PN532_I2C = Pn532I2c(1)
nfc = Pn532(PN532_I2C)

def setup():
    nfc.begin()
    versiondata = nfc.getFirmwareVersion()
    if not versiondata:
        raise RuntimeError("Could'nt find a board")

    print("Found chip PN5 {:#x} Firmware ver. {:d}.{:d}".format((versiondata >> 24) & 0xFF, (versiondata >> 16) & 0xFF,
                                                                (versiondata >> 8) & 0xFF))
    nfc.setPassiveActivationRetries(0xFF)
    # configure board to read RFID tags
    nfc.SAMConfig()
    print("Waiting for an ISO14443A card")

def loop():
    success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)

    if (success):
        time.sleep(1)
        card_id = '-'.join(f'{n:02X}' for n in uid)
        print(f"Found a card, length: {len(uid)}")
        print(f"Card: {card_id}")
        return True
    else:
        print("Timed out waiting for a card")
        return False

if __name__ == '__main__':
    setup()
    while 1:
      loop()
