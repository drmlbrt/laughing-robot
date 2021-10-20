# import cli
import json
def check_if_info_in_file(file_name, info_to_search):
    """ Check if any line in the file contains given string """
    # Open the file in read only mode
    for index, line in enumerate(file_name):
        # Read all lines in the file one by one
        for split_line in line.split(" "):
            # print(split_line)
            if split_line.find(info_to_search, 0) == 0:
                dummy_line = file_name[index]
                return dummy_line


vlan990= """
Vlan990                10.242.67.16    YES DHCP   up                    up
"""
versioninformation = """Cisco IOS XE Software, Version 16.11.01
Cisco IOS Software [Gibraltar], Catalyst L3 Switch Software (CAT9K_IOSXE), Version 16.11.1, RELEASE SOFTWARE (fc3)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2019 by Cisco Systems, Inc.
Compiled Thu 28-Mar-19 09:42 by mcpre
Cisco IOS-XE software, Copyright (c) 2005-2019 by cisco Systems, Inc.
All rights reserved.  Certain components of Cisco IOS-XE software are
licensed under the GNU General Public License ("GPL") Version 2.0.  The
software code licensed under GPL Version 2.0 is free software that comes
with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
GPL code under the terms of GPL Version 2.0.  For more details, see the
documentation or "License Notice" file accompanying the IOS-XE software,
or the applicable URL provided on the flyer accompanying the IOS-XE
software.
ROM: IOS-XE ROMMON
BOOTLDR: System Bootstrap, Version 16.12.2r, RELEASE SOFTWARE (P)
EoIP3-OSW-9300-BL uptime is 1 day, 19 hours, 17 minutes
Uptime for this control processor is 1 day, 19 hours, 19 minutes
System returned to ROM by Reload Command at 12:13:08 UTC Wed Sep 29 2021
System image file is "flash:packages.conf"
Last reload reason: Reload Command
This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.
A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html
If you require further assistance please contact us by sending email to
export@cisco.com.
Technology Package License Information:
------------------------------------------------------------------------------
Technology-package                                     Technology-package
Current                        Type                       Next reboot
------------------------------------------------------------------------------
network-advantage       Smart License                    network-advantage
dna-advantage           Subscription Smart License       dna-advantage
AIR License Level: AIR DNA Advantage
Next reload AIR license Level: AIR DNA Advantage
Smart Licensing Status: UNREGISTERED/EVAL MODE
cisco C9300-24U (X86) processor with 1411676K/6147K bytes of memory.
Processor board ID FOC2351U1A1
2 Virtual Ethernet interfaces
28 Gigabit Ethernet interfaces
8 Ten Gigabit Ethernet interfaces
2 TwentyFive Gigabit Ethernet interfaces
2 Forty Gigabit Ethernet interfaces
2048K bytes of non-volatile configuration memory.
8388608K bytes of physical memory.
1638400K bytes of Crash Files at crashinfo:.
11264000K bytes of Flash at flash:.
0K bytes of WebUI ODM Files at webui:.
Base Ethernet MAC Address          : 4c:e1:75:a1:b9:80
Motherboard Assembly Number        : 73-18272-04
Motherboard Serial Number          : FOC23509DV8
Model Revision Number              : A0
Motherboard Revision Number        : A0
Model Number                       : C9300-24U
System Serial Number               : FOC2351U1A1
Switch Ports Model              SW Version        SW Image              Mode
------ ----- -----              ----------        ----------            ----
*    1 41    C9300-24U          16.11.1           CAT9K_IOSXE           INSTALL
Configuration register is 0x102
"""
facts = {
        "Vlan990_ip": "",
             "Version": "",
             "Hostname": ""
    }

hostname = "hostname EoIP3-OSW-9300-BL"
str_hostname = list(filter(len, hostname.split(' ')))
facts["Hostname"] = str_hostname[1]
split_versioninformation = versioninformation.splitlines()
str_list = list(filter(len, vlan990.split(' ')))
print(str_list)
print(str_list[1] +  " is in status " + str_list[4] )

facts["Vlan990_ip"]= str_list[1]

find_words = ["Version"]

for word in find_words:
    if check_if_info_in_file(split_versioninformation, word):
        version = check_if_info_in_file(split_versioninformation, word)
        print(version)
        facts["Version"] = version
    else:
        print('Info not found in file')
print(json.dumps(facts))

json_facts = json.dumps(facts)

json_object = json.loads(json_facts)
print(json_object["Hostname"])

