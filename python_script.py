import cli
import time
import datetime
from itertools import count
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import io

tftp_server = '10.15.255.52'
http_server = '10.15.255.52'
smtp_server = "10.8.145.37"
cfgfile = "baseline.cfg"
eoipfile = "eoip.py"
tarfile = "Tcl.tar"
destination_running_config = 'running-config'
flash_guest_share = "flash:guest-share/"
flash = "flash:"
tftp_server_provisioned_devices = "10.15.255.52/9K/provisioned_devices/"
ios = "cat9k_iosxe.17.03.03.SPA.bin"
n = datetime.datetime.today().strftime('%Y-%m-%d')
d = datetime.datetime.today().strftime('%Y-%m-%d:%H-%M-%S')

counter = count(1)

def fixed_length_string(_string):
    if len(_string) <= 100:
        shortage = 100 - len(_string)
        fixed_length_string = "CodeDebugLine__"+str(next(counter))+"__"+d+"__"+(shortage * "=")+(_string)+"\n"
        return fixed_length_string


def check_if_info_in_file(file_name, info_to_search):
    """ Check if any line in the file contains given string """
    # Open the file in read only mode
    for index, line in enumerate(file_name):
        # Read all lines in the file one by one
        for split_line in line.split(" "):
            # print(fixed_length_string(split_line)
            if split_line.find(info_to_search, 0) == 0:
                dummy_line = file_name[index]
                print(fixed_length_string(dummy_line))
                return dummy_line


def _test_reachability(*args):
    pass

def get_facts():
    facts = {
        "Vlan990_ip": "",
        "Version": "",
        "Hostname": ""
    }
    hostname = cli.execute('sh run | i hostname')
    vlan990 = cli.execute('show ip interface brief | i Vlan990')
    versioninformation = cli.execute('show version | i Version')
    split_versioninformation = versioninformation.splitlines()
    str_hostname = list(filter(len, hostname.split(' ')))
    facts["Hostname"] = str_hostname[1]
    str_list = list(filter(len, vlan990.split(' ')))
    facts["Vlan990_ip"] = str_list[1]
    find_words = ["Version"]
    for word in find_words:
        if check_if_info_in_file(split_versioninformation, word):
            version = check_if_info_in_file(split_versioninformation, word)
            facts["Version"] = version
        else:
            print(fixed_length_string('Info not found in file'))
        return facts


def install_guestshell_network():
    device_facts = get_facts()
    print(fixed_length_string("\nINSTALLING THE GUESTSHELL NETWORKING CONFIGURATION"))
    subnet = [i for i in device_facts["Vlan990_ip"].split(".")]
    vlan990_subnet = (subnet[2])
    try:
        cli.configure(["app-hosting appid guestshell",
                       "app-vnic AppGigabitEthernet trunk",
                       "vlan 990 guest-interface 0",
                       "guest-ipaddress 10.242.%s.10 netmask 255.255.255.192" % (vlan990_subnet),
                       "app-default-gateway 10.242.%s.1 guest-interface 0" % (vlan990_subnet),
                       "name-server0 10.8.69.33"])
        print(fixed_length_string("\nFINISHED INSTALLING THE GUESTSHELL NETWORKING CONFIGURATION"))
    except Exception as e:
        # Print any error messages to stdout
        print(fixed_length_string(e))
        return


def confirm_installation():
    device_facts = get_facts()
    filename = "/bootflash/guest-share/%s_%s_.txt" % (n, device_facts["Vlan990_ip"])
    file = "%s_%s_.txt" % (n, device_facts["Vlan990_ip"])
    try:
        with open(filename, "a") as my_file:
            my_file.write("\n================================================================\n")
            my_file.write("\n===== This is an Auto generated ZeroTouchInstallation file =====\n")
            my_file.write("\nDate:" + n)
            my_file.write("\n================================================================\n")
            my_file.write(str(device_facts))
            my_file.write("\n================================================================\n")
            my_file.close()
            try:
                # "copy flash:guest-share/2021-12-13_10.242.67.16_.txt tftp://10.15.255.52/9K/provisioned_devices/2021-12-13_10.242.67.16_.txt"
                cli.execute("copy flash:guest-share/%s tftp://%s%s" % (file, tftp_server_provisioned_devices, file))
                print(fixed_length_string("\n"))
                print(fixed_length_string("\nCREATING PROVISIONING SUCCESS FILE"))
            except Exception as e:
                # Print any error messages to stdout
                print(fixed_length_string(e))
                return
    except Exception as e:
        # Print any error messages to stdout
        print(fixed_length_string(e))
        return


def download(*args, destination):
    while True:
        try:
            for file in args:
                cli.execute("ping %s" % (tftp_server))
                print(fixed_length_string("\nBEGINNING TRANSFER FOR %s FILE " % (file)))
                cli.executep("copy tftp://%s/9K/%s %s" % (tftp_server, file, destination))
                time.sleep(0.2)
                print(fixed_length_string("\nTRANSFER %s FILE OK " % (file)))
                if file == str(tarfile):
                    cli.execute("archive tar /xtract flash:Tcl.tar flash:")
                return
        except:
            print(fixed_length_string("\nTRANSFER %s FILE *FAILED* " % (file)))
            return


def monitoring():
    print(fixed_length_string("\n Configuring SNMP settings"))
    time.sleep(0.5)
    try:
        cli.configurep(["ip access-list standard ACL_SNMP", "permit 10.0.0.0 0.255.255.255"])
        cli.configurep(["snmp-server group SNMP_GROUP_READ v3 priv",
                        "snmp-server trap-source Vlan990",
                        "snmp-server source-interface informs Vlan990",
                        "snmp-server contact CCV&C TechBu Deployed Networks",
                        "snmp-server user SNMP_USER_READ SNMP_GROUP_READ v3 auth SHA *** priv AES 128 *** access ACL_SNMP"
                        ])
    except Exception as e:
        # Print any error messages to stdout
        print(fixed_length_string(e))
        return


def checkflash():
    check_flash = cli.executep('dir flash:*.bin')
    index = check_flash.find(ios)
    if index >= 0:
        print(fixed_length_string("The IOS XE download succeeded "))
        print(fixed_length_string("The Flash: contains the correct version "))
        print(fixed_length_string('Changing to new IOS XE version '))
    else:
        print(fixed_length_string("Download has not finished yet, waiting 5 minutes "))
        time.sleep(15)
    return


def baseline():
    print(fixed_length_string("\nStarting Baseline Installation "))
    cli.executep("term no mon")
    time.sleep(0.2)
    print(fixed_length_string("\nManagement VLAN is set "))
    cli.configurep(["file prompt quiet", "ip tftp blocksize 1468"])
    cli.configurep(["crypto key generate rsa label KP_SSH mod 2048"])
    cli.configurep(["alias exec EOIPpy guestshell run python /flash/eoip.py"])
    time.sleep(0.2)
    download(tarfile, eoipfile, destination=flash)
    download(cfgfile, destination=destination_running_config)
    print(fixed_length_string("\nStarting Monitoring Installation "))
    monitoring()
    print(fixed_length_string("\nStarting Update IOS Installation "))
    try:
        confirm_installation()
        return
    except Exception as e:
        # Print any error messages to stdout
        print(fixed_length_string(e))
        print(fixed_length_string("\nEMAIL ERROR )> EMAIL NOT SEND "))
    return


def main():
    print(fixed_length_string('\nSwitch Baseline Install '))
    baseline()
    print(fixed_length_string('\nPreparing email with device facts switch '))
    cli.execute('copy running-config startup-config')
    print(fixed_length_string('\nDevice Installation with Zero Touch Finished '))
    print(fixed_length_string('\nThere is no shame in doing a COPY RUN START '))
    return


if __name__ in "__main__":
    main()
