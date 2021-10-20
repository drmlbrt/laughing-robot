import cli

def baseline():
    cli.executep('copy tftp://ip/iosxe/9k/eoip-osw-9300-baseline-cfg_V3.0.cfg running-config')
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
        sleep(5)
    return

def updateios():
    cli.executep('copy tftp://ip/iosxe/9k/cat9k_iosxe.17.03.03.SPA.bin flash:')
    # is the new version there?
    checkflash()
    return

def siteconfig():
    cli.configurep(["hostname ZTP-OSW-UNSET", "end"])
    return

def checkversion():
    version = cli.executep('show version')
    expectedversion = '16.11.01'
    index = version.find(expectedversion)
    if index >=0:
        print("version is valid for IOS XE 16.11.01")
    else:
        updateios()
    return

print('---- Starting with the Version Check of the Device. This can take some time.')
checkversion()
print('---- IOS Check Finished')
print('---- Switch Baseline Install')
baseline()
print('---- Switch SiteConfiguration')
siteconfig()
print('---- Contacting central server through router')
cli.executep('copy running-config startup-config')
print('---- Device Installation with Zero Touch Finished')
exit()