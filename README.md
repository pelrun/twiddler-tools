PS/2 twiddler keymap utils
==========================

Requires the Construct python library.

Currently converts a Twiddler 2.1 keymap (created by the java configurator tool) into a Twiddler 2.0 eeprom image.

Run with:

python keymapper.py <twiddler config file>

it will output the following files:

keymap.bin: raw 8k eeprom image.
upload.bin: For uploading with the twiddler's rs232 mode. Need to do the "PTwiddler" manually before uploading this.
buspirate.txt: script to program the eeprom using a buspirate.

PS2 upload on my Twiddler didn't work the cable was busted, and I don't have a Win98 box to run the official ancient keymap tool.
RS232 upload didn't work: my Twiddler didn't write more than the first 0x400 bytes or so.
I ended up connecting a Bus Pirate and uploading that way. Note: for this to work, you have to pull the microcontroller out of the socket! Otherwise it keeps the EEPROM in write protect mode.

Sorry for the awful code (especially the EEPROM generation, which I can't seem to map completely in Construct), it'll get refactored at some point.
