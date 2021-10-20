import time
import sys
from pprint import pprint
#import cli


def toolbar():
    toolbar_width = 70

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

def zeroize():
    cli.configurep(["no pnp profile pnp-zero-touch","crypto key zeroize", "no crypto pki certificate pool"])
    cli.executep("delete /force vlan.dat")
    toolbar()
    cli.executep("delete /force nvram:*.cer")
    toolbar()
    cli.executep("delete /force stdb-nvram:*.cer")
    cli.executep("write erase")
    print("\n####---- Please Type MANUALY - R E L O A D - then type 'NO' --------####")
    return

def macro():
    return

def siteconfig():
    sitename = input('####---- Provide SITE TRIGRAM XXX:  ')
    oswnumber = input('####---- Provide SWITCH NUMBER XXX:  ')
    print('\n####---- This is the ne Site Name : OSW-%s-%s' %(sitename, oswnumber))
    happy = str(input('\n####---- Are you happy ? : YES/NO : '))
    if happy.lower() in ["y","yes"]:
        toolbar()
        print("#" * 67)
        print('You have typed YES - Configuring Hostname')
        print("#" * 67)
        cli.configurep(["ip hostname OSW-%s-%s" %(sitename, oswnumber)])
        toolbar()
        cli.executep('wr')
        return
    else:
        print("#" * 67)
        print('You have typed NO')
        print("#" * 67)
        return

def menu():
    while True:
        print("=" * 67)
        menudict={
                1: "Change Switch Name - Site Config",
                2: "Zeroize the switch config",
                3: "Exit the program",
            }
        data = sorted([(k, v) for k, v in menudict.items()])
        pprint(data)
        print("=" * 67)
        choice = int(input("What do you like to do?: ")) or int('1')

        print("=" * 67)
        if choice == 1:
            print("You have selected Process %s : %s" %(choice,(menudict[choice])))
            siteconfig()
        elif choice == 2:
            print("You have selected Process %s : %s" %(choice,(menudict[choice])))
            zeroize()
        elif choice == 9:
            print("You have selected Process %s : %s" %(choice,(menudict[choice])))
            text = ("--- Thank you and please come again ---")
            print(text)
            exit()
        else:
            text = ('invalid option, check you input. It needs %s' %(choice))
            print(text)

def main():
    print('\n####---- Welcome to the EoIP Script - Python -  -------------------------------------###')
    print('\n####---- Baseline is OK     ---------------------------------------------------------###')
    menu()
    cli.executep('copy running-config startup-config')
    return

if __name__ in "__main__":
    main()