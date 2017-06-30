# ZigBee Enabled PYTHON-SBC-SDK-PYTHON
**Paasmer ZigBee Enabled IoT SDK - Python** for Single Board Computers Running Linux

## Overview

The **Paasmer ZigBee Enabled Python SDK** for **Single Board Computers (SBC)** like Raspberry-PI, Intel Edison, Beagle Bone is a collection of source files that enables you to connect to the Paasmer IoT Platform and remotely monitor our devices with the help of ZigBee protocol. It includes the transport client for **MQTT** with **TLS** support.  It is distributed in source form and intended to be built into customer firmware along with application code, other libraries and RTOS.

## Features

The **Paasmer ZigBee Enabled Python SDK** simplifies access to the Pub/Sub functionality of the **Paasmer IoT** broker via **MQTT**. The **SDK** has been tested to work on the **Raspberry Pi 3** running Raspbian Jessie connected to an **Arduino UNO** board through **ZigBee**. Support for Other SBC's running any flavours of Linux would be available shortly.

## MQTT Connection

The **Paasmer ZigBee Enabled Python SDK** provides functionality to create and maintain a mutually authenticated TLS connection over which it runs **MQTT**. This connection is used for any further publish operations and allow for subscribing to **MQTT** topics which will call a configurable callback function when these topics are received.

## Pre-Requisites

Registration on the portal http://developers.paasmer.co, is necessary to connect the devices to the **Paasmer IoT Platform**.The SDK has been tested on the Raspberry PI 3 with Raspbian Jessie (https://downloads.raspberrypi.org/raspbian_latest) 

* Raspberry PI 3 Model B Board.

* Arduino UNO Board.

* 2 ZigBee modules.

* XCTU Software installed on your system (https://www.digi.com/products/xbee-rf-solutions/xctu-software/xctu) for ZigBee configuration.

* Arduino IDE installed on your system (https://www.arduino.cc/en/main/software)

# Installation

* Download the SDK or clone it using the command below.

```
$ git clone https://github.com/PaasmerIoT/ZBee-Py-SBC-SDK.git
$ cd SBC-SDK-PYTHON
```

## ZigBee Configuration

To establish, the ZigBee protocol the 2 ZigBee modules are to configured as a Coordinator and a Router. The ZigBee at the Raspberry PI side is to be configured as a Coordinator and the one at the Arduino side as a Router. Use XCTU software to Configure the ZigBee's as explained in the `ZigBEE_config.pdf` file.

The installation part is to be done in two parts, like

* Arduino  

* Raspberry 
 
## Arduino 

* Connect the ZigBee Router device to the Arduino UNO as give below

| Arduino   | XBee |
| --------- | -----|
| 5V        | 5V   |
| GND       | GND  |
| TX        | RX   |
| RX        | TX   |


* Open a new Sketch, Copy and Paste from the `ZigBee.ino` file in `<Arduino Sketch_DIR>/`.

* Connect the Arduino UNO board to your system, open the Arduino IDE and click on the `TOOLS` icon, select the `Board` as **Arduino/Genuino UNO** and select the port in which the board is connected in the `Port` option. 


* Edit the pins as per your requirement

```
int pin[3]={7,8,9,4};
int control[]={10,11};
```

* Save and Run the code in Arduino UNO.
 
## Raspberry PI 

* To connect the device to Paasmer IoT Platform, the following steps need to be performed.

```
$ cd /paasmer-iot-device-sdk-python/
$ sudo ./install.sh
```

* Upon successful completion of the above command, the following commands need to be executed.

```
$ sudo su
$ source ~/.bashrc
$ PAASMER
$ sed -i 's/alias PAASMER/#alias PAASMER/g' ~/.bashrc
$ exit
```


* Edit the config.h file to include the user name(Email), device name, feed names and GPIO pin details.

```
UserName = "XXXXXXX" #your user name used in developer.paasmer.co for registration
DeviceName = "YYYYY" #your device name
feedname1 = "TemprSensor" #feed name used for displaying in the developer.paasmer.co This feed is restricted to temprature sensor
feedtype1 = "Distance"
feedname2 = "Soil moisture sensor" #feed name used for display in the developer.paasmer.co this feed is restricted to digital sensor
feedtype2 = "digital" # type should be in ['temp','digital']
feedname3 = "Proxmity" #feed name used for display in the developer.paasmer.co this feed is restricted to digital sensor
feedtype3 = "" # type should be in ['temp','digital'] for Temprature sensor we have buld a functionality fo fetch temprature directly
feedname4 = "Water level sensor" #feed name used for displaying in the developer.paasmer.co, This Feed is restricted to Distance sensor(Ultrasonic)
feedtype4 = "distance" #Please do not edit this line
controlfeedname1 = "sprinkler" #feed name used for display in the developer.paasmer.co
controlfeedname2 = "water_motor" #feed name used for display in the developer.paasmer.co
timePeriod = 5 #change the time delay(in seconds) as you required for sending sensor values to paasmer cloud
```

* Connect the ZigBee Coordinator device to the Raspberry PI through the USB2.0 cable.

* Go to the directory below.

```
$ cd samples/basicPubSub/
```

* Edit the following in the `basicPubSub.py` file 

* Use the command below and press tab to find which port the XBee is connected to the Raspberry PI board.

```
ls -lrt /dev/tty
```

* Now edit the USB port number in the following line in the `BasicPubSub.py` file.

```
ser = serial.Serial("/dev/ttyUSB*",9600)
``` 

* Edit the Path of the SDK and Certifications as given below. 

```
sys.path.append('/home/pi/SBC-SDK-PYTHON')

# Read in command-line parameters
useWebsocket = False
host = "a3rwl3kghmkdtx.iot.us-west-2.amazonaws.com"
rootCAPath = "/home/pi/SBC-SDK-PYTHON/certs/rootCA.crt"
certificatePath = "/home/pi/SBC-SDK-PYTHON/certs/e76b102a41-certificate.pem.crt"
privateKeyPath = "/home/pi/SBC-SDK-PYTHON/certs/e76b102a41-private.pem.key"
```
   
* Run the code using the command below.

```
$ sudo python basicPubSub.py
```

* The device would now be connected to the Paasmer IoT Platform and publishing sensor values are specified intervals.

## Support

The support forum is hosted on the GitHub, issues can be identified by users and the Team from Paasmer would be taking up requests and resolving them. You could also send a mail to support@paasmer.co with the issue details for the quick resolution.

## Note

* The Paasmer IoT SBC-SDK-PYTHON utilises the features provided by AWS-IOT-SDK for Python.
