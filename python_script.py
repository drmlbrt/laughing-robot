import cli
import time

tftp_server = '10.120.202.7'
cfgfile = "eoip-osw-9300-baseline-cfg_V3.0.cfg"
destination = 'running-config'
destinationflash="flash:"
ios = "cat9k_iosxe.17.03.03.SPA.bin"

def set_managementinterface():
    cli.configurep(["int vlan 990", "ip address dhcp", "end"])
    time.sleep(60)
    return

def baseline():
    cli.configurep(["file prompt quiet", "ip tftp blocksize 8192"])
    cli.executep("copy tftp://%s/%s %s vrf Mgmt-vrf" %(tftp_server, cfgfile, destination))
    time.sleep(60)
    return

def checkflash():
    checkflash = cli.executep('dir flash:*.bin')
    expectedversion = 'cat9k_iosxe.17.03.03.SPA.bin'
    index = checkflash.find(expectedversion)
    if index >= 0:
        print("---- The download succeeded")
        print("---- The Flash: contains the correct version")
        print('---- Changing the startup IOS to new version')
        cli.configurep(["boot flash:cat9k_iosxe.17.03.03.SPA.bin", "end"])
    else:
        print("---- Download is not yet finished, waiting 5 minutes")
        time.sleep(60)
    return

def updateios():
    cli.executep("copy tftp://%s/%s %s vrf Mgmt-vrf" %(tftp_server, ios, destinationflash))
    # is the new version there?
    checkflash()
    time.sleep(60)
    return

def siteconfig():
    cli.configurep(["hostname ZTP-OSW-UNSET", "end"])
    time.sleep(10)
    return

def checkversion():
    version = cli.executep('show version')
    expectedversion = '16.11.01'
    index = version.find(expectedversion)
    if index >=0:
        print("---- version is valid for IOS XE 16.11.01")
    else:
        updateios()
    return

def main():
    print('---- Starting with the Version Check of the Device. This can take some time.')
    print('---- IOS Check Finished')
    print('---- Switch Baseline Install')
    baseline()
    print('---- Switch SiteConfiguration')
    siteconfig()
    print('---- Contacting central server through router')
    cli.executep('copy running-config startup-config')
    print('---- Device Installation with Zero Touch Finished')
    return



if __name__ in "__main__":
    main()