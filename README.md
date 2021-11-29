# Iridium SBC

Iridium offers a number of data services. Apart from an internet dial-up data service, there is also a short 
message service called Iridium Short Burst Data (SBD).

SBD is a bandwidth-limited messaging system, capable of transmitting packets of up to 340 bytes, and receiving packets of 270 bytes.

SBD is suitable for applications which need to regularly send or receive small amounts of information - typically these would include tracking, telemetry, system control and monitoring applications.

It is not suitable if very low latency is required, or if the data to be transmitted is larger than a few thousand bytes. Sending images, or GRIB files, is usually not sensible.

With a good view of the sky, it is possible to send/receive approximately once every 10 seconds.


## Iridium 9602

The 9602/9602N is a single board transceiver provided as a ‘black box’ transceiver module with all device interfaces  provided  by a 
single multi-pin interface connector in addition to the antenna connector.

Key Features:
- Single board transceiver.
- Small form factor.
- Aluminum alloy casework (LM2 / LM24) with Alodine 2600 passivation coating.
- No SIM card.
- Designed to be incorporated into an OEM solution.
- Maximum mobile originated message size 340 bytes.
- Maximum mobile terminated message size 270 bytes.
- Automatic Notification to the Transceiver that a mobile terminated message is queued at the Gateway.
- Global operating capability
- RoHS compliant

### Serial Data Interface

The Serial data interface is used to both command the 9602/9602N and transfer user data to and from the Transceiver. The 9602/9602N 
presents a 9-wire data port to the FA (Field Application), where the interface is at 3.3V digital signal levels.

By default, the serial interface operates as a 9-wire connection, The serial interface may be operated with a 3-wire connection, where
only transmit, receive and ground signals  are  used.  However  the  9  wire  interface  offers  better  control  and  is  the  
recommended implementation. Iridium is only able to provide limited 3-wire interface support. Due to the small code space and limited
processing resources of the 9602/9602N the flow control is limited.
 
When operating with a 3-wire connection, the following rules apply: 
 
- AT&Dn must be set to AT&D0 to ignore the DTR input
- AT&Kn must be set to AT&K0 to disable RTS/CTS flow control
- The other output signals may be connected, and operate as follows: 
	- CTS driven ON (low) 
	- DSR operates as normal 
	- RI operates as normal 
	- DCD driven ON (low)


## Iridium 9603

The 9603/9603N is a single board transceiver provided as a ‘black box’ transceiver module with all device interfaces provided by a 
single multi-pin interface connector in addition to the antenna connector.

Key Features:
- Single board transceiver 
- Small form factor 
- No SIM card 
- Designed to be incorporated into an OEM solution 
- Maximum mobile originated message size 340 bytes 
- Maximum mobile terminated message size 270 bytes 
- Automatic Notification to the Transceiver that a mobile terminated message is queued at the Gateway 
- Global operating capability 
- RoHS compliant

The 9603/9603N is configured and operated through the use of AT commands. See the 
[“ISU AT Command Reference”](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwibtcbmn670AhWehP0HHdyvD3EQFnoECAUQAQ&url=https%3A%2F%2Fwww.beamcommunications.com%2Fdocument%2F328-iridium-isu-at-command-reference-v5&usg=AOvVaw3JcNmRmEgJsIaUPvivEPXI) 
for the full set of AT commands and responses. Note that versions 3.2 and earlier of the ISU AT Command 
Reference do not mention the 9603/9603N. Subsequent versions of the reference will do so.


## RockBLOCK

RockBLOCK makes it easy to use Iridium Short-Burst Data (SBD) services with your project.

The PCB assembly hosts an Iridium SBD transceiver, simplifies the power requirements, and provides a serial interface to your project.
RF considerations are taken care of by RockBLOCK's built-in antenna, or SMA connector for an external antenna.

RockBLOCK makes it easy to use Iridium Short-Burst Data (SBD) services with your project.

RockBLOCKS come in three different versions - the RockBLOCK 9602, RockBLOCK 9603 and RockBLOCK Plus.

### RockBLOCK 9602

The original version of RockBLOCK was based on the Iridium 9602 module. This module was superseded by the 9603N, which is 
significantly smaller and functionally equivalent. Rock Seven still manufactures the RockBLOCK 9602 to support existing applications, 
but it is strongly recommended that new projects use the RockBLOCK 9603.


### RockBLOCK 9603

RockBLOCK 9603 is designed to host the Iridium 9603N module, and is as small as is practically possible. The minimum size is defined 
by the ground plane required for the 25mm patch antenna. It is powered by 5V DC and has a UART interface.

This latest version has an on-board patch antenna, and an SMA connector for an external antenna. The unit is configured to use either 
the patch or external antenna at assembly time, using a small RF link. It is possible for a competent end user to switch between the 
patch and external antenna - see Switching RockBLOCK 9603 antenna mode for more information on how to do so.


#### Serial interface

With your RockBLOCK connected to a suitable power supply, check that your serial communications are established.

```bash
$ lsusb -t
/:  Bus 02.Port 1: Dev 1, Class=root_hub, Driver=xhci_hcd/4p, 5000M
/:  Bus 01.Port 1: Dev 1, Class=root_hub, Driver=xhci_hcd/1p, 480M
    |__ Port 1: Dev 2, If 0, Class=Hub, Driver=hub/4p, 480M
        |__ Port 1: Dev 3, If 0, Class=Vendor Specific Class, Driver=ftdi_sio, 12M
```

default baudrate 19200, 8N1

```bash
sudo minicom -b 19200 -D /dev/ttyUSB0
```

and issue the following commands
```text
/* Issue AT command */

AT\r

/* Receive response */

OK\r

/* Turn off Flow Control */

AT&K0\r

/* Receive response */

OK\r

/* Insert ASCII message into MO buffer */

AT+SBDWT=Hello World\r 

/* Receive response */

OK\r

/* Initiate an Extended SBD Session */

AT+SBDIX\r

/* Receive response */ 

+SBDIX: <MO status>, <MOMSN>, <MT status>, <MTMSN>, <MT length>, <MT queued>\r

/* See SBDIX Key for information on each parameter */
```


## CLI tool

This repo contains the source code for a CLI that interacts with the Iridium SDB Rockboards (both 9602 and 9603 versions).

### Installation

It is always recommended the creation of a python virtual environment.

``` bash
python3 -m venv venv
```

``` bash
source venv/bin/activate
```

``` bash
pip install -e src
```

### Usage

``` bash
(venv) pi@raspberrypi:~ $ iridium-sbd
Usage: iridium-sbd [OPTIONS] COMMAND [ARGS]...

Options:
  --serial_device TEXT  Serial device path.
  --help                Show this message and exit.

Commands:
  send
  signal
  receive
```

At the moment, two operations are supported only:

- Showing signal bar

```bash
(venv) pi@raspberrypi:~ $ iridium-sbd signal

Status                  | (0, 68, 0, -1, 0, 0)
Model                   | IRIDIUM 9600 Family SBD Transceiver
Call Processor Version  | TA13001        
Modem DSP Version       | 1.7 svn        
CpeM DSP Version        | 1.2 svn        
CpeA DSP Version        | 1.2 svn        
DBB Version             | 0x0001 (ASIC)  
RFA Version             | 0x0004 (2A)    
NVM Version             | KVS            
Hardware Version        | BOOT07d2/9602revG/04/RAW04
BOOT Version            | TA13001 (rev 3525)
Serial Number           | 300234063233380
Geolocation             | (4056, 228, 4896) 2021-11-26T13:30:52Z
System time             | 2021-11-26T15:42:56Z

Press CTR+C to exit

Signal  [##############                      ]  2/5
```

- Sending a text message


```bash
(venv) pi@raspberrypi:~ $ iridium-sbd send --message "Hello from space!"
Status                  | (0, 68, 0, -1, 0, 0)
Model                   | IRIDIUM 9600 Family SBD Transceiver
Call Processor Version  | TA13001
Modem DSP Version       | 1.7 svn
CpeM DSP Version        | 1.2 svn
CpeA DSP Version        | 1.2 svn
DBB Version             | 0x0001 (ASIC)
RFA Version             | 0x0004 (2A)
NVM Version             | KVS
Hardware Version        | BOOT07d2/9602revG/04/RAW04
BOOT Version            | TA13001 (rev 3525)
Serial Number           | 300234063233380
Geolocation             | (4056, 228, 4896) 2021-11-26T13:30:52Z
System time             | 2021-11-26T15:52:17Z
Talking to satellite...
0 (32, 68, 2, 0, 0, 0)
1 (32, 68, 2, 0, 0, 0)
2 (32, 68, 2, 0, 0, 0)
3 (32, 68, 2, 0, 0, 0)
4 (32, 68, 2, 0, 0, 0)
5 (0, 67, 0, 0, 0, 0)

DONE.
```

- Receiving a text message

```bash
(venv) pi@raspberrypi:~ $ iridium-sbd receive
Status                  | (0, 69, 0, -1, 0, 0)
Model                   | IRIDIUM 9600 Family SBD Transceiver
Call Processor Version  | TA13001        
Modem DSP Version       | 1.7 svn        
CpeM DSP Version        | 1.2 svn        
CpeA DSP Version        | 1.2 svn        
DBB Version             | 0x0001 (ASIC)  
RFA Version             | 0x0004 (2A)    
NVM Version             | KVS            
Hardware Version        | BOOT07d2/9602revG/04/RAW04
BOOT Version            | TA13001 (rev 3525)
Serial Number           | 300234063233380
Geolocation             | (4056, 224, 4900) 2021-11-26T15:56:21Z
System time             | 2021-11-29T14:13:35Z
Talking to satellite...
0 (32, 69, 2, 0, 0, 0)
1 (32, 69, 2, 0, 0, 0)
2 (32, 69, 2, 0, 0, 0)
3 (32, 69, 2, 0, 0, 0)
4 (32, 69, 2, 0, 0, 0)
5 (32, 69, 2, 0, 0, 0)
6 (32, 69, 2, 0, 0, 0)
7 (32, 69, 2, 0, 0, 0)
8 (0, 69, 1, 1, 8, 0)

DONE.
Hello RB

```

## References

- https://usermanual.wiki/Iridium-Satellite/9603N.Iridium-9602-9602N-SBD-Transceiver-Developers-Guide-V1-2--DRAFT2/html
- https://usermanual.wiki/Iridium-Satellite/9603N.Developers-guide/html
- https://www.datawell.nl/Portals/0/Documents/Brochures/datawell_brochure_iridium_sbd_b-40-03.pdf
- https://docs.rockblock.rock7.com/docs/getting-started
- https://www.youtube.com/watch?v=NOJ_VtSikAA
