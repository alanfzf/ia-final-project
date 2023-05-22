#include <Wire.h>
#include <SPI.h>
#include <Adafruit_PN532.h>

/*
  PINOUT:
  MOSI <---> D7
  MISO <---> D6
  SCK <---> D5
  SS <---> D4
*/
#define PN532_SCK  14
#define PN532_MOSI 13
#define PN532_SS   2
#define PN532_MISO 12

Adafruit_PN532 nfc(PN532_SCK, PN532_MISO, PN532_MOSI, PN532_SS);

void setup(void) {
  Serial.begin(115200);
  nfc.begin();

  uint32_t versiondata = nfc.getFirmwareVersion();
  if (!versiondata) {
    Serial.print("Didn't find PN53x board");
    while (1); // halt
  }

  // Got ok data, print it out!
  Serial.print("Found chip PN5"); Serial.println((versiondata>>24) & 0xFF, HEX);
  Serial.print("Firmware ver. "); Serial.print((versiondata>>16) & 0xFF, DEC);
  Serial.print('.'); Serial.println((versiondata>>8) & 0xFF, DEC);

  nfc.setPassiveActivationRetries(0xFF);
}

void loop(void) {
  boolean success;
	// Buffer to store the returned UID
  uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };
  // Length of the UID (4 or 7 bytes depending on ISO14443A card type)
  uint8_t uidLength;

  success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, &uid[0], &uidLength);

  if (success) {
    Serial.printf("Tarjeta encontrada\n");

    for(int i = 0; i < uidLength; i++){
       Serial.printf("%02X-", uid[i]);
    }

    Serial.println();
   	delay(1000);
  }
  else
  {
    // PN532 probably timed out waiting for a card
    Serial.println("Timed out waiting for a card");
  }
}

char* getTag(uint8_t uidLen, uint8_t uid[]){
  char* result = {};
  return result;
}
