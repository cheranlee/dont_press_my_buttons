# dont_press_my_buttons

### Inspiration
Elevator congestion is a daily occurance in NUS' Residential Colleges (RCs). With only three elevators to service over 540 pax, students often spend upwards of 2 minutes waiting for their elevator to arrive. To reduce this, residents are advised to practice good elevator etiquette by not pressing consecutive floors, and instead climbing up/down one floor to their destination. However, this etiquette is not always followed, to the annoyance of many residents.

### What it does
Our project seeks to address poor elevator etiquette by using social pressure and minor daily annoyances to motivate residents not to press consecutive floors in the elevator.

The elevator's travel patterns are tracked using a microcontroller-controlled camera. Images of the elevator's display panel (@ Level 1 Lobby) are streamed through an artificial intelligence software (optical character recognition) to detect which floors the elevator stops at. Offending floors (those who frequently press consecutive floors) are identified, and the following actions are taken:

The floor numbers are "named and shamed" via a telegram bot (that can be added into the RC's chat groups), and
"Annoyance devices" are installed on each floor beside the lift. On offending floors, the device will play annoying tones and flash warning lights whenever a resident passes by, hence physically reminding them to practice proper elevator ettiquette.

### How we built it
The system is built around the Espressif 32 (ESP-32/ESP-Cam) microcontrollers, which are programmed using Arduino and Platformio IDE.

The ESP-Cam (camera-enabled ESP-32) is mounted at the Level 1 lift lobby, where it streams a video of the lift's LCD display showing the current floor.
Optical character recognition is implemented using pytesseract in Python to identify the current floor
Python is also used to automatically identify the offending floors, control the telegram bot, and activate the "annoyance devices".
