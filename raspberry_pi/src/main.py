import time
from pn532pi import Pn532, Pn532I2c, pn532
from picam import RaspCam

nfc = Pn532(Pn532I2c(1))
cam = RaspCam()

def setup():
    nfc.begin()
    time.sleep(2)
    ver_data = nfc.getFirmwareVersion()

    if not ver_data:
        raise RuntimeError("Could not find a board")

    chip = (ver_data >> 24) & 0xFF
    v1,v2 = (ver_data >> 16) & 0xFF, (ver_data >> 8) & 0xFF

    print(f"Found chip PN5 {chip:#x} Firmware ver. {v1:d}.{v2:d}")

    nfc.setPassiveActivationRetries(0xFF)
    nfc.SAMConfig()
    print("Card setup done, waiting for a card...")

def loop():
    success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)

    if success:
        card_id = '-'.join(f'{n:02X}' for n in uid)
        print(f"Found a card ({card_id}), length: {len(uid)}")
        resp = cam.send_info(card_id)
        print(resp)
        time.sleep(5)

if __name__ == '__main__':
    setup()
    while True:
      loop()
