# TV-B-Gone on HiP Badge with ESP32-C3 -- and also HOPE_16 badge with ESP32-C3 -- and also ESP32 WEMOS D1 MINI with ESP32-S3

We want to add TV-B-Gone to the HiP Badge from 2022 with an aim of using it on the HOPE_16 badge which is derived from the HiP badge.  

I also want to make a new version of the TV-B-Gone kit, which is easier to solder, and easier to re-program.  I am thinking of using an ESP32 module.  It can compile and be re-programmed with the Arduino software.

The Arduino sketch here works.

## Functionality
When you click the NA or EU pushbutton:  
.....quickly blink the visible LED 3x for NA and 6x for EU  
.....for all codes for the given region (NA or EU):  
........blip the visible LED  
........grab the info for the next POWER-Code from WORLDcodes.cpp  
........transmit the POWER-Code on the IR LED (using the ESP32 LEDC library for PWM)  
........delay 205 msec  
........If the EU or NA push-button is pushed while transmitting the database of POWER-Codes,  
...............then start transmitting the entire sequence again from the beginning.  
........quickly blink the visible LED 3x for NA and 6x for EU  

## Hardware
  The circuit (external for the ESP32 WEMOS D1 MINI, or built-in for the HOPE badge Rel. 0.8.14):  
  - IR LED connected to digital output pin 2 through an NPN (2N3904) digital current amplifier:  
       -- Emitter to GND  
       -- Base through a 1K resistor to digital output pin 2  
       -- Collector to 47 Ohm resistor to IR LED to +3.3V (LED Anode to +3.3V)  
  - Visible LED connected to digital output pin 13 to ground through 1K resistor  
  - NA pushbutton attached between digital input pin 10 and GND (with 10K pullup resistor):  
       -- pullup resistor: use internal 10K resistor (connected from digital input pin 10 to 3.3V)  
  - EU pushbutton attached between digital input pin 9 and GND (with 10K pullup resistor):  
       -- pullup resistor: use internal 10K resistor (connected from digital input pin 9 to 3.3V)  
