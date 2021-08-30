# laughing-robot
###zero_touch_provisioning_for_cisco_devices

Laughing Robot is a name proposed by GitHub, per coincidence I rather like it. 
The overall goal is to provide ZERO TOUCH PROVISIONING to the new Cisco 9K infrastructure. 
This provisioning has the objective of not touching the switches manually...

Easy said, someone has to connect the device to the network where it receives a DHCP address by the 
system. So DHCP is the key in provinding the switch with the needed intelligence.
This intelligence is provided by a Python script that is downloaded via the DHCP options.
The script is automating manual procedures.

Basically:
######ref:
https://developer.cisco.com/docs/ios-xe/#!day-zero-provisioning-quick-start-guide/zero-touch-provisioning-ztp

Code Snippit to start:

```
ip dhcp pool ztp_device_pool                            <-- Name of DHCP pool
    vrf Mgmt-vrf                                            <-- Management VRF
    network 10.1.1.0 255.255.255.0                        <-- Range of client IP addresses
    default-router 10.1.1.1                                <-- Gateway address
    option 150 ip 203.0.113.254                            <-- Script server
    option 67 ascii /sample_python_dir/python_script.py  <-- Python script name
````

option 150: tftp server, may be a list of devices
option 67: location of the script on the tftp server, I think only one ? 

#####DHCP ? 
 



###Script
First, remember that the python terminal is opened first. That is what I understood of the documentation. 
What happens, the switch boots up until it reaches the automated prompt : do you like to configure the devices with the wizard yes/no
Also, it is a basic terminal on the switch. So you can't import Python Modules. This depends on your company security restrictions.


You have to be patient, after some time the device automatically arrives at the auto boot. It shall check for connected interfaces and if they receive
a dhcp address. 
Inside the DHCP there are two options (150&67) that connect and download the script.

Example script:
````buildoutcfg
print "\n\n *** Sample ZTP Day0 Python Script *** \n\n"

 # Importing cli module
 import cli

print "\n\n *** Executing show version *** \n\n"
 cli.executep('show version')

print "\n\n *** Configuring a Loopback Interface *** \n\n"
 cli.configurep(["interface loop 100", "ip address 10.10.10.10 255.255.255.255", "end"])

print "\n\n *** Executing show ip interface brief *** \n\n"
 cli.executep('show ip int brief')

print "\n\n *** ZTP Day0 Python Script Execution Complete *** \n\n"
````
The fact is, it opens the python inside the switch. 
>Question: is this Python 3.0?

###Replacing the man 

The basic script I would like to have should:
- recognize the current ios, if not valid, download new
- download the - baseline config 
- check the connected SUBNET ?
    - change the NAME in accordance with the SET
    - Add VLAN information (Management)
- connection test 
- verification configuration

###The Switch
Basic Version out of the box:
````commandline
Cisco IOS XE Software, Version 16.11.01
Cisco IOS Software [Gibraltar], Catalyst L3 Switch Software (CAT9K_IOSXE), Version 16.11.1, RELEASE SOFTWARE (fc3)
#The Switch Hardware# May differ depending on the delivery
Model Number                       : C9300-24U
````
####Enabling the guestshell
````commandline
LBD-DIS-9300-01#guestshell run python
 iox feature is not enabled
LBD-DIS-9300-01(config)#iox
LBD-DIS-9300-01(config)#end
LBD-DIS-9300-01#show iox-service
------'wait a minute'------
IOx Infrastructure Summary:
---------------------------
IOx service (CAF)    : Running
IOx service (HA)     : Running
IOx service (IOxman) : Running
Libvirtd             : Running
````
You need to enable a 'virtual interface' on the device. Found this on the whitepapers.
````commandline
LBD-DIS-9300-01#guestshell enable
Interface will be selected if configured in app-hosting
Please wait for completion
% Error: No interface configuration for guestshell
LBD-DIS-9300-01#conf t
LBD-DIS-9300-01(config)#app-hosting appid guestshell
LBD-DIS-9300-01(config-app-hosting)#app-vnic management guest-interface 0
LBD-DIS-9300-01(config-app-hosting-mgmt-gateway)#end
LBD-DIS-9300-01#guestshell enable
Interface will be selected if configured in app-hosting
Please wait for completion
guestshell activated successfully
Current state is: ACTIVATED
guestshell started successfully
Current state is: RUNNING
Guestshell enabled successfully

LBD-DIS-9300-01#guestshell run python
Python 2.7.5 (default, Apr 11 2018, 07:36:10)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-28)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>>

````
Look at the default. Python 2.7.5
The documentation says that Python 3 is present on the device. I wonder? 
Answer = NOT

Let's start with sketching.

###Enabling ZTP on a pre-configured switch - LAB env.

````commandline
configure terminal
    no pnp profile pnp-zero-touch
    crypto key zeroize
    no crypto pki certificate pool
    end
delete /force vlan.dat
delete /force nvram:*.cer
delete /force stby-nvram:*.cer
write erase
reload
   ---> answer no when it asks you to save configuration ! 
````
##What should happen

When a device that supports Zero-Touch Provisioning boots up, and does not find the startup configuration (during fresh install on Day Zero), 
the device enters the Zero-Touch Provisioning mode. The device locates a Dynamic Host Control Protocol (DHCP) server, bootstraps itself 
with its interface IP address, gateway, and Domain Name System (DNS) server IP address, and enables Guest Shell. 
The device then obtains the IP address or URL of a TFTP server, and downloads the Python script to configure the device.

## I guess
LBD-ISR-E301-01(config)#pnp startup-vlan 990
This should be enabled to allow ZTP/PnP on the router through VLAN 990. The default is VLAN 1; which is disabled 
on this system.

And... magic.
After the weekend I stumbled upon this: %Error opening tftp://10.120.202.12//9K/python_script.py (Time
Bad path from me, and the tftp server was offline. 

After correction:

````commandline
Would you like to enter the initial configuration dialog? [yes/no]: guestshell installed successfully
Current state is: DEPLOYED
guestshell activated successfully
Current state is: ACTIVATED
guestshell started successfully
Current state is: RUNNING
Guestshell enabled successfully


HTTP server statistics:
Accepted connections total: 0  File "/bootflash/downloaded_script.py", line 10
    cli.executep(f"copy tftp://{ip}/eoip-osw-9300-baseline-cfg_V3.0.cfg running-config ")
                                                                                       ^
SyntaxError: invalid syntax
````

So I made the script in Python 3.0 syntax. I remembered that the Python Shell starts in default 2.7. How to solve this?
After changing the script syntax:

````commandline
Current state is: DEPLOYED
guestshell activated successfully
Current state is: ACTIVATED
guestshell started successfully
Current state is: RUNNING
Guestshell enabled successfully


HTTP server statistics:
Accepted connections total: 0---- Starting with the Version Check of the Device. This can take some time.
---- IOS Check Finished
---- Switch Baseline Install
Line 1 SUCCESS: file prompt quiet
Line 2 SUCCESS: ip tftp blocksize 8192

%Log packet overrun, PC 0x7F76D4DCC604, format:
User:%s  logged command:%s

%Log packet overrun, PC 0x7F76D4DCC604, format:
User:%s  logged command:%s
Accessing tftp://10.120.202.7/eoip-osw-9300-baseline-cfg_V3.0.cfg...
Loading eoip-osw-9300-baseline-cfg_V3.0.cfg from 10.120.202.7 (via GigabitEthernet0/0): !
[OK - 42522 bytes]
42522 bytes copied in 22.435 secs (1895 bytes/sec)
---- Switch SiteConfiguration
Line 1 SUCCESS: hostname ZTP-OSW-UNSET
Line 2 SUCCESS: end
---- Contacting central server through router
Building configuration...
[OK]
---- Device Installation with Zero Touch Finished

````
Perfect.
In the end, the only limits are your scripting talents. 
It has proven that with little setup you can run the ZeroTouch Provisioning without any issues. 



