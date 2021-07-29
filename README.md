# Hiking Computer with SOS function

Koray Amico Kulbay (ka223ek)

## Project overview
Embarking on an adventure in nature often has you wondering about the conditions around you. Thanks to this hiking computer a user can know the local altitude, temperature and humidity with access to an SOS functionality.

### Time needed
~ 5 hours (If you have experience from an introductionary course in IoT)

## Objective
The project was actually chosen as a solution to a specific sensor issue that made me abandon my first idea of a free diving computer. Although the purpose of this hiking computer is very similar, as it measure the same physical properties (pressure, humidity and temperature).

I think that a hiking computer of this sort wil orient a user and connect them more to their hiking experience, as they will constantly know at which altitude they're at together with humidity and temperature. The SOS functionaliy will serve as an extra layer of security. 

## Material

All parts in the table appear in the same order (left to right) as pictures below.

| Part | Specification |Purchase location | Cost [SEK]|
| -------- | -------- | -------- |-------- |
| Pycom FiPy     | Development board     | RS components     |732     |
| Pycom Universal Expansion Board     | Provides easy USB, battery and pin access to the FiPy     | RS components     |247      |
| Pycom Universal Antenna Kit      | Enables wireless network connectivity     | RS components     |130     |
| LiPo Battery     | Portable power source     | Electrokit     |249     |
| DHT11 sensor     | Temperature and humidity sensor     | Electrokit     |49     |
| Push button     | Enables a physical interface with the FiPy     | Electrokit     |19     |
| BMP280 sensor     | Temperature and pressure sensor     | ELAB     |18     |
| SSD1306 OLED display     | Displays symbols on a 128x32 pixel display     | ELAB     |16     |
| Breadboard     | Easy way to connect sensors to the expansion board     | Electrokit     |69     |
| Micro-USB cable    | Connects FiPy to a computer via the expansion board     | Electrokit     |39     |
| Jumper cables    | Connects the components to the breadboard     | Electrokit     |39     |

![](https://i.imgur.com/dFJp8KX.png =100x100) ![](https://i.imgur.com/1nuh3oq.png =100x100) ![](https://i.imgur.com/HsUgZ44.png =100x100) ![](https://i.imgur.com/kRG5z6U.jpg =100x) ![](https://i.imgur.com/1tutFyt.jpg =100x100) ![](https://i.imgur.com/Rzem79o.jpg =100x) ![](https://i.imgur.com/OJiy4AJ.png =100x100) ![](https://i.imgur.com/4uTrGAr.jpg =100x100) ![](https://i.imgur.com/IhHUhlY.jpg =100x100) ![](https://i.imgur.com/hANkqSV.jpg =100x100) ![](https://i.imgur.com/8502Kiv.jpg =100x100)

## Computer setup 
0. Connect the FiPy to the expansion board (LED of the FiPy towards the micro-USB port) and then connect it all to your computer with a micro-USB cable.
1. Download the [Pycom Device Firmware Updater](https://docs.pycom.io/updatefirmware/device/) and update your FiPy to the latest pybytes version. (An issue that might arise is not being able to connect with Pymakr later in this tutorial. I found a solution where you use an older update version at this step - use pybytes version 1.20.1 and tick "Erase during update".)
2. [Install Node.js](https://nodejs.org/en/) on your computer.
3. [Install VS Code](https://code.visualstudio.com/docs/setup/setup-overview) on your computer.
4. Setup the [Pymakr extension](https://docs.pycom.io/gettingstarted/software/vscode/) in VS Code. 

### Why VS Code as IDE?
VS Code was chosen for this project as it has a very conventient way of adding custom functionality. It's called extensions and we use it to install the Pymakr extension which is a smart and easy way to manage uploaded code to the FiPy device. 

### File structure of Pycom devices
![](https://i.imgur.com/mHnU7fY.png)

You keep the main code you want to run in `main.py` and all libraries in the `lib` folder (libraries are used for sensor and long code that can be called upon from `main.py`).

### How to use the Pymakr extension

![](https://i.imgur.com/V9NxVa0.png)
Thanks to the pymakr extension installed in step 4 above we get this easy-to-use graphical interface to use the FiPy device. When you want code to run on the FiPy that is written in `main.py` you click the upload button, then `main.py` should automatically run on your FiPy. If you want to interrupt the code you can press CTRL-C and to rerun the same code you can click the run button. 

## Sensor connection
![](https://i.imgur.com/H8CfEFU.png)

|   Sensor    |    Data input     |
|:-----------:|:-----------------:|
|    DHT11    |        P23        |
| Push button |        P16        |
|   BMP280    | SDA: P9, SCL:P10  |
|   SSD1306   | SDA: P9, SCL:P10  |
|   SSD1306   | SDA: P11, SCL:P12 |

- Different sensors need a different power supply voltage as seen in the diagram. The orange cables represent 3.3 Volts and the red 5.5 Volts. 
- Looking at the diagram above one can notice two different I2C buses (protocol used for more complex sensors). On the first I2C bus (SDA on pin 9 and SCL on pin 10) the BMP280 sensor and one SSD1306 display is connected. The reason why a second SSD1306 display is connected to its own I2C bus is because two identical displays would occupy exactly the same address on an I2C bus, which would force them to display the same values. Another way of having two identical and independent sensors/displays but on the same I2C bus is to change the adress manually of one sensor/display in the software. 
- This setup is currently only for development, one would need to solder to use this in production. 

## Platform - Ubidots
This project uses Ubidots as a platform, but Amazon Web Services and Pybytes were also tested. The reason Ubidots finally was used was because it has more features than Pybytes but is **a lot** simpler to use than AWS.

Ubidots is a great cloud based alternative that is free for educational use. One can collect data from many devices and summarize it all in "dashboards" which gives a clean data presentation. One important functionality is "Events" as one can send emails, text messages, Discord messages and more if measured values reach a certain level. This is exactly what is needed for the SOS feature of the Hiking Computer. 

Scaleing the Hiking Computer would definitely be possible regarding adding more sensors as the educational plan of Ubidots allows up to 20 measured values per device. But if many hiking computers are supposed to be deployed, that can be an issue as only 3 devices can be used for free. 

### Correct setup
Go to the [Ubidots webpage](https://industrial.ubidots.com/accounts/signup_industrial/) and create a Ubidots STEM account. 

## Network - Sigfox
### Why Sigfox?
There exists many different networks. Examples are Bluetooth, WiFi, LoRaWAN, Sigfox and more. Since the hiking computer is supposed to be used outside, long range networks are needed that doesn't need too much power. This left only LoRaWAN and Sigfox, since the LoRaWAN coverage was not good where I live that left Sigfox as the only reasonable option. The only con with it is that it costs money to use, but with a new Pycom device one year of subscription is included. 

### Correct setup
**IMPORTANT!:** Do not attempt to use any Sigfox functionality without attaching the antenna to your FiPy, otherwise your device might be beyond rescue!
1. Register your Pycom device for the 1 year free subscription according to [this](https://docs.pycom.io/gettingstarted/registration/sigfox/) tutorial.
2. Log in to your [Sigfox backend](https://backend.sigfox.com/auth/login) account and click on the "DEVICE" tab at the navigation bar. Click on the "Id" name and then on the "MESSAGES" tab on your left navigation bar. Here we will look for our very first message sent over Sigfox. 
3. Run the following script in your `main.py` just to make sure that everything is set up correctly: 
```python
from network import Sigfox
import socket

# init Sigfox for RCZ1 (Europe)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)

# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

# make the socket blocking
s.setblocking(True)

# configure it as uplink only
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

# send some bytes
s.send(bytes([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]))
```
4. Something similar to this should show up in your "MESSAGES" window in Sigfox backend: ![](https://i.imgur.com/swhFRSm.png)


## Bridge between the network and the platform
All that is left now is to redirect the data from your Sigfox account to your Ubidots account. 
1. Log in to your [Sigfox backend](https://backend.sigfox.com/auth/login) account again. 
2. Click on the "DEVICE" tab, click on the "Device type" in the list, click on the "CALLBACKS" tab to your left, click "New" to your top right and finally click "Custom callback".
3. Insert the following:![](https://i.imgur.com/mux4ycI.png)

4. Next to "x-auth-token" paste in your Ubidots default token which can be found in your Ubidots account according to this image:![](https://i.imgur.com/f8Cc9UT.png)
5. Click "OK".



## The code
The full repo can be found [here](https://github.com/kurreman/Hiking-Computer). And the file structure looks like this: ![](https://i.imgur.com/4sQHUxE.png)

The main file is structured very simple and consists of two parts. The very first "code snippet" sets up the correct environment to send data via Sigfox. The second part uses this environment and collects data that gets sent to the Sigfox network.
`main.py`:
```python
from SIGFOX import setup_sigfox
from data_gathering import gather_data

#SIGFOX SETUP
s = setup_sigfox()
#Data gathering
gather_data(s)
```

`gather_data(s)` does the following:
1. Sets up the correct I2C buses and pins to read the sensor data. 
2. Displays a welcome message to the user on display one.
3. Collects altitude (converted from absolute pressure), temperature and humidity (data) every 2 seconds. During this time it also checks if the button is being pressed.
4. If it's not pressed it will check if there has been at least 10 minutes since data got sent to Sigfox and will send data if that's the case.  
5. If the button is pressed it calls for a helper function that checks if the button is being pressed at least three times with an interval of two seconds. If that happens it will send data to Sigfox together with an SOS value that has Ubidots send an alert email to me. 

### Converting pressure to altitude
```python
def altitude_from_pressure(pressure):
    """Returns altitude in meters with pressure input in Pascal"""

    P_SL = 101325 # Pascal
    T_SL = 15 + 273.15 #K
    L = -0.0065 # [K/m]
    h_SL = 0 #m
    R = 8.31432 #Nm/molK
    g = 9.80665 #m/s^2
    M = 0.0289644 #kg/mol

    h = h_SL + (T_SL/L)*((pressure/P_SL)**((-R*L)/(g*M))-1)
    return h
```
This function is implemented correctly, but might produce strange results. This has more to do with the BMP280 sensor and it probably needs some calibration. This is left for the future exploration of the project and will not be addressed during the course of applied IoT. 

### Sensor libraries
Complex sensors, especially I2C ones, need libraries to function properly. The following third party libraries were used: 



| Library | Source |
| -------- | -------- |
| `bmp280.py`     | [HERE](http://www.learnmicropython.com/esp32/bmp280-barometric-pressure-sensor-micropython-example.php#codesyntax_1)     |
| `dht.py`     |  [HERE](https://github.com/JurassicPork/DHT_PyCom)      |
| `ssd1306.py`     | [HERE](https://github.com/robert-hh/pycom-micropython-sigfox/blob/homebrew/drivers/display/ssd1306.py)     |


## Connectivity
Since Sigfox uses public radio frequencies each device is limited to 1% of the data sent according to European regulations. This means that a device can send approx. 140 messages per day which is almost the same as one message per 10 minutes, which is exactly how often the Hiking Computer sends data. Sigfox uses their own lightweight transport protocol which increases battery life of connected devices. 

### Data types sent

The following code reveals that the temperature, humidity, altitude and sos value is sent as four bytes where each byte is a little endian integer: 
```python
s.send(struct.pack("<B", int(round(temperature)))+struct.pack("<B",int(humidity))+struct.pack("<B",int(round(altitude)))+struct.pack("<B",0))
```
where s is a socket object according to this code of the file `SIGFOX.py`:
```python
from network import Sigfox
import socket

def setup_sigfox():
    """Sets up a Sigfox connection """
    # init Sigfox for RCZ1 (Europe)
    sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)

    # create a Sigfox socket
    s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

    # make dht11e socket blocking
    s.setblocking(True)

    # configure it as uplink only
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False) # False if only uplink
    return s
```

## Presenting the data
When using the free Ubidots STEM license the data is saved for 1 month on the cloud database. Since it's in the cloud it's constantly saving the data that is sent. 

To create a dashboard click on the "Data" tab and select "Dashboards" in the drop down menu. Click on the left hand menu and then the "+" sign to add a Dashboard. Once it's created click on the right hand plus sign to add widgets. When setting up the widgets, different variables can be selected according to what's have been sent after the first sent data from your Hiking Computer. The dashboard eventually looks like this when the SOS signal is inactivated: ![](https://i.imgur.com/3m0kATL.png)

And like this when the SOS signal is active: ![](https://i.imgur.com/1M8wd6Z.png)

### Setting up the SOS alarm
Click on the "Data" tab and select "Events" in the drop down menu. Click the blue "+" sign to your top right. Set it up like this: ![](https://i.imgur.com/swxM3OW.png) Then choose the email function, which email to contact and what the email should say. 

## Finalizing the design
This is the greeting a user is welcomed with upon start up of the computer: ![](https://i.imgur.com/QX6kViV.jpg)

This is how the data is presented locally and how the user is notified when data is sent over Sigfox: 
![](https://i.imgur.com/tAE1Smw.jpg)

This is what the displays show after the button has been pressed to send an SOS signal over Sigfox: 
![](https://i.imgur.com/3UIZUCv.jpg)

which results in the following email being received: 
![](https://i.imgur.com/5s9j7Vm.png)

## The future of the hiking computer
As mentioned in the introduction of this tutorial this project was supposed to be a free diving computer, but due to no micropython library existing for the pressure sensor that could handle water pressure that stopped the initial idea. It will still be done, but when I can put time into designing an I2C library for the other pressure sensor from the datasheet. 

Regarding the hiking computer there's already plans in action to 3D print a case and connect the battery to make the project mobile. The progress will be updated into this markdown file, so feel free to keep an eye out :). 

## Acknowledgements
I'd like to express my gratitude to all the TA's for excellent help and endless patience, I once even received help during a Saturday! 

I'd also like to thank the teachers Fredrik Ahlgren and Francis Palma for a super fun and well planned course! I learned so much that I've always wanted to know! 