import cli
import time
import datetime
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import io


file_server = '10.15.255.52'
smtp_server = "10.8.145.37"
cfgfile = "baseline.cfg"
eoipfile = "eoip.py"
tarfile = "Tcl.tar"
destination = 'running-config'
destinationflash = "flash:"
ios = "cat9k_iosxe.17.03.03.SPA.bin"
n = datetime.datetime.today().strftime('%Y-%m-%d')


def check_if_info_in_file(file_name, info_to_search):
    """ Check if any line in the file contains given string """
    # Open the file in read only mode
    for index, line in enumerate(file_name):
        # Read all lines in the file one by one
        for split_line in line.split(" "):
            # print(split_line)
            if split_line.find(info_to_search, 0) == 0:
                dummy_line = file_name[index]
                print(dummy_line)
                return dummy_line


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
            print('Info not found in file')
        return facts


def installguestshellnetworking():
    device_facts = get_facts()
    print("\n####----------------INSTALLING THE GUESTSHELL NETWORKING CONFIGURATION --------###")
    subnet = [i for i in device_facts["Vlan990_ip"].split(".")]
    vlan990_subnet = (subnet[2])
    cli.configure(["app-hosting appid guestshell",
                   "app-vnic AppGigabitEthernet trunk",
                   "vlan 990 guest-interface 0",
                   "guest-ipaddress 10.242.%s.10 netmask 255.255.255.192" % (vlan990_subnet),
                   "app-default-gateway 10.242.%s.1 guest-interface 0" % (vlan990_subnet),
                   "name-server0 10.8.69.33"])
    print("\n####-------FINISHED INSTALLING THE GUESTSHELL NETWORKING CONFIGURATION --------###")
    return


def confirminstallation():
    my_file = io.StringIO()
    device_facts = get_facts()
    filename = "%s-%s.cfg" %(n,device_facts["Vlan990_ip"])
    try:
        my_file.write("=====================================================")
        my_file.write("This is an Auto generated ZeroTouchInstallation file:")
        my_file.write("Date:" + n)
        my_file.write("=====================================================")
        my_file.write(str(device_facts))
        my_file.close()
    except Exception as e:
        # Print any error messages to stdout
        print(e)
        return


def toolbar():
    toolbar_width = 86
    # setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))  # return to start of line, after '['
    for i in range(toolbar_width):
        time.sleep(0.05)  # do real work here
        # update the bar
        sys.stdout.write("#")
        sys.stdout.flush()
    sys.stdout.write("]\n")  # this ends the progress bar
    return


def snmp():
    print("\n---- Configuring SNMP settings")
    time.sleep(0.5)
    cli.configurep(["ip access-list standard ACL_SNMP", "permit 10.0.0.0 0.255.255.255"])
    cli.configurep(["snmp-server group SNMP_GROUP_READ v3 priv",
                    "snmp-server trap-source Vlan990",
                    "snmp-server source-interface informs Vlan990",
                    "snmp-server contact CCVC TechBu Deployed Networks",
                    "snmp-server user SNMP_USER_READ SNMP_GROUP_READ v3 auth SHA SNMPPASS priv AES 256 SNMPPASS access ACL_SNMP"
                    ])
    toolbar()
    return


def download(*args, destination):
    while True:
        try:
            for file in args:
                cli.execute("ping %s" % (file_server))
                print("\n----#### BEGINNING TRANSFER FOR %s FILE ####----" % (file))
                cli.executep("copy http://%s/9K/%s %s" % (file_server, file, destination))
                time.sleep(0.2)
                toolbar()
                print("\n----#### TRANSFER %s FILE OK ####----" % (file))
                if file == str(tarfile):
                    cli.executep("archive tar /xtract flash:Tcl.tar flash:")
                    toolbar()
                return
        except:
            print("\n----#### TRANSFER %s FILE *FAILED* ####----" % (file))
            return


def monitoring():
    print("\n---- Configuring SNMP settings")
    time.sleep(0.5)
    cli.configurep(["ip access-list standard ACL_SNMP", "permit 10.0.0.0 0.255.255.255"])
    cli.configurep(["snmp-server group SNMP_GROUP_READ v3 priv",
                    "snmp-server trap-source Vlan990",
                    "snmp-server source-interface informs Vlan990",
                    "snmp-server contact CCVC TechBu Deployed Networks",
                    "snmp-server user SNMP_USER_READ SNMP_GROUP_READ v3 auth SHA SNMPPASS priv AES 128 SNMPPASS access ACL_SNMP"
                    ])
    toolbar()
    return


def checkflash():
    checkflash = cli.executep('dir flash:*.bin')
    index = checkflash.find(ios)
    if index >= 0:
        print("----#### The IOS XE download succeeded")
        print("----#### The Flash: contains the correct version")
        print('----#### Changing to new IOS XE version')
    else:
        print("----#### Download has not finished yet, waiting 5 minutes")
        time.sleep(15)
    return


def updateios():
    version = cli.execute('show version')
    expectedversion = '17.03.03'
    index = version.find(expectedversion)
    if index >= 0:
        print("----#### version is valid for IOS XE %s" % (expectedversion))
    else:
        cli.execute("install remove inactive")
        cli.configure("boot system flash:packages.conf")
        download(ios, destination=destinationflash)
        checkflash()
        cli.execute("install add file flash:%s activate commit" % (ios))
    return


def baseline():
    print("\n----#### Starting Baseline Installation---------------------------------------------------###")
    cli.executep("term no mon")
    time.sleep(0.2)
    print("\n----#### Management VLAN is set-----------------------------------------------------------###")
    cli.configurep(["file prompt quiet", "ip tftp blocksize 1468"])
    cli.configurep(["crypto key generate rsa label KP_SSH mod 2048"])
    cli.configurep(["alias exec EOIPpy guestshell run python /flash/eoip.py"])
    toolbar()
    time.sleep(0.2)
    download(cfgfile, eoipfile, destination=destination)
    download(tarfile, destination=destinationflash)
    print("\n----#### Starting Monitoring Installation-------------------------------------------------###")
    monitoring()
    print("\n----#### Starting Update IOS Installation-------------------------------------------------###")
    updateios()
    try:
        confirminstallation()
        return
    except Exception as e:
        # Print any error messages to stdout
        print(e)
        print("\n####--------------- EMAIL ERROR )> EMAIL NOT SEND ----------------------------###")
    return

def main():
    print('\n####---- Switch Baseline Install ----------------------------------------------------###')
    baseline()
    print('\n####---- Preparing email with device facts switch -----------------------------------###')
    cli.execute('copy running-config startup-config')
    print('\n####---- Device Installation with Zero Touch Finished -------------------------------###')
    print('\n####---- There is no shame in doing a WRITE MEM  :-)  -------------------------------###')
    return


if __name__ in "__main__":
    main()
