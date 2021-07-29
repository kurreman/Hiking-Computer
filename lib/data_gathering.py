#SSD1306 OLED Display
from machine import Pin, I2C
import ssd1306
import time
from bmp280 import BMP280
from dht import DHT # https://gidht11ub.com/JurassicPork/DHT_PyCom
import struct
from altitude import altitude_from_pressure

def sos_counter(counter=1):
    """Checks if the button is pressed 3 times within 2 seconds of each button press and returns True if thats the case. """
    sos = False
    old_time = time.time()
    push_button = Pin('P16', mode = Pin.IN)
    while time.time()-old_time < 2:
        button_val = push_button()
    old_time = time.time()
    if button_val == 0 and time.time()-old_time <= 2:
        if counter < 3:
            counter +=1
            sos = sos_counter(counter)
        else:
            return True
    else:
        return False
    return sos


def gather_data(s):
    """Main code where the device reads and interacts with sensors data."""
    #I2C PROTOCOL SETUP
    i2c = I2C(0, pins=('P9','P10'))     # Using default pins for SDA P9 and SCl P10
    #Display 1
    display = ssd1306.SSD1306_I2C(128, 32, i2c)

    #Display 2
    i2c_2 = I2C(1, pins=('P11','P12'))
    display2 = ssd1306.SSD1306_I2C(128, 32, i2c_2)

    #Pressure sensor
    bmp280 = BMP280(i2c)
    #Button 
    push_button = Pin('P16', mode = Pin.IN)  # SENSOR BUTTON FORM ELEKTROKIT
    #Humidity and temp sensor
    dht11 = DHT(Pin('P23', mode=Pin.OPEN_DRAIN), 0)
    #time.sleep(2)

    #Greeting
    display.text("WELCOME TO", 10, 0, 1)
    display.text("KURRY-NET", 10, 10, 1)
    display.text("HIKING COMPUTER", 0, 20, 1)
    display.show()
    time.sleep(10)
    display.fill(0)
    display.show()

    #FUNCTIONALITY
    time_last_Sigfox_upload = time.time() - 10*60 #Subtraction such that we start sending data to Sigfox straight away
    while True:
        
        dht11_result = dht11.read()
        while not dht11_result.is_valid():
            time.sleep(.5)
            dht11_result = dht11.read()
            print("Forever")
            display2.text("forever",0,0,1)
            display2.show()

        button_val = push_button() # get value, 0 or 1
        pressure = bmp280.pressure #Pa
        altitude = altitude_from_pressure(pressure) #m
        temperature = dht11_result.temperature #°C
        humidity = dht11_result.humidity #%

        display.fill(0)
        display.show()

        display.text('Temp.:{}C'.format(temperature), 0, 0, 1)
        display.text('Hum.:{}%'.format(humidity), 0, 10, 1)
        display.text('Alt.:{}m'.format(round(altitude)), 0, 20, 1)
        display.show()

        if button_val == 0:
            display2.fill(0)
            display2.show()
            display2.text("Entered SOS mode", 0, 0, 1)
            display2.show()
            sos = sos_counter()
            print("SOS is {}".format(sos))
            if sos:
                test = s.send(struct.pack("<B", int(round(temperature)))+struct.pack("<B",int(humidity))+struct.pack("<B",int(round(altitude)))+struct.pack("<B",1))
                print(test)
                display2.text("SOS sent", 10, 10, 1)
                display2.show()
                time.sleep(5)
            elif not sos:
                display2.fill(0)
                display2.show()

        if time.time() - time_last_Sigfox_upload > 10*60:
        # send values as little-endian and int
            test2 = s.send(struct.pack("<B", int(round(temperature)))+struct.pack("<B",int(humidity))+struct.pack("<B",int(round(altitude)))+struct.pack("<B",0))
            print(test2)
            time_last_Sigfox_upload = time.time()
            display2.text("DATA SENT", 0, 0, 1)
            display2.show()
            time.sleep(10)
            display2.fill(0)
            display2.show()
        else:
            time.sleep(2) #Important to sleep in order to avoid invalid result for the DHT11 sensor

