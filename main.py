from machine import Pin, I2C
import utime
from ssd1306 import SSD1306_I2C
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20
utime.sleep(2)
trigger = Pin(0, Pin.OUT)
echo = Pin(1, Pin.IN)
in1 = Pin(14, Pin.OUT)
in2 = Pin(15, Pin.OUT)
in3 = Pin(27, Pin.OUT)
in4 = Pin(26, Pin.OUT)
led = Pin(25, Pin.OUT)

WIDTH =128
HEIGHT= 64
i2c=I2C(0,scl=Pin(17),sda=Pin(16),freq=200000)
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)
write15 = Write(oled, ubuntu_mono_15)
write20 = Write(oled, ubuntu_mono_20)
        
def forward():
    in1.value(0)
    in2.value(1)
    in3.value(0)
    in4.value(1)
    
def backward():
    in1.value(1)
    in2.value(0)
    in3.value(1)
    in4.value(0)

def left():
    in1.value(0)
    in2.value(1)
    in3.value(0)
    in4.value(0)
    
def stop():
    in1.value(0)
    in2.value(0)
    in3.value(0)
    in4.value(0)
    
def ultra():
   trigger.low()
   utime.sleep_us(2)
   trigger.high()
   utime.sleep_us(5)
   trigger.low()
   while echo.value() == 0:
       signaloff = utime.ticks_us()
   while echo.value() == 1:
       signalon = utime.ticks_us()
   timepassed = signalon - signaloff
   distance = (timepassed * 0.0343) / 2
   print("The distance from object is ",distance,"cm")
   return distance


def move_with_sensor():
   total_left = 0
   total_count = 0

   while ultra() > 45:
      forward()
      utime.sleep(.2)
      led.toggle()
      total_count += 1
      oled.fill(0)
      write20.text("WALLE", 0, 0)
      write20.text("Clear", 0, 20)
      write15.text('I can continue', 0, 40)
      oled.show()
      print(total_count)
      if total_count % 200 == 0:
         backward()
         utime.sleep(1)
         left()
         utime.sleep(1)
         total_count = 0   
   while ultra() < 45 and ultra() > 15:
       if in1.value() == 0 and in2.value() == 1 and in3.value() == 0 and in4.value() == 1:
          stop()
          utime.sleep(.5)
       left()
       utime.sleep(.5)
       total_left += 1
       print("my continous left count is: " + str(total_left))
       oled.fill(0)
       write20.text("WALLE", 0, 0)
       write20.text("Caution", 0, 20)
       write15.text('Turn Left', 0, 40)
       oled.show()
       if total_left == 20:
          backward()
          utime.sleep(.75)
          left()
          utime.sleep(.75)
       
   while ultra() <= 15:
       backward()
       utime.sleep(.5)
       oled.fill(0)
       write20.text("WALLE", 0, 0)
       write20.text("Stop", 0, 20)
       write15.text('Danger ahead', 0, 40)
       oled.show()

while True:
   try:
      move_with_sensor()
      
   except KeyboardInterrupt:
      in1.value(0)
      in2.value(0)
      in3.value(0)
      in4.value(0)
      led.value(0)
      break