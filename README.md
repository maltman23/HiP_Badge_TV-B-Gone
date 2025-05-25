# Adding TV-B-Gone to HiP Badge with ESP32 C3

We want to add TV-B-Gone to the HiP Badge from 2022 with an aim of using it on the HOPE_16 badge which is derived from the HiP badge.  

I have a working TV-B-Gone sketch that compiles and uploads and functions well on Arduino boards, programmed with the Arduino IDE.

The Initial Commmit is the same as my working Arduino sketch, except:  
* PROGMEM statements were taken out (since with ESP on Arduino IDE, I see from others on the internet that constants remain in program memory, unike with Arduino code)  
* updated comments  
  
The code in the initial commit runs out of memory, which indicates to me that I am not presenting things correctly for the ESP32 on Arduino environment, 
since the ESP32 has more memory than an ATmega328 chip.  
