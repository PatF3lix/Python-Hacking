import subprocess
import optparse
import re

# to run this program, you must run it with sudo privileges. sudo python mac_changer

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="new MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("Please specify an interface. use --help for more info")
    if not options.new_mac:
        parser.error("Please specify a new MAC address. use --help for more info")
    return options

def change_mac(interface, new_mac):
    command = "ifconfig"
    subprocess.call([command, interface, "down"])
    subprocess.call([command, interface, "hw", "ether", new_mac])
    subprocess.call([command, interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode('utf-8'))
    if mac_address_result:
        return(mac_address_result.group(0))
    else:
        print("[-] Could not read mac address")

def print_result(options, current_mac):
    if current_mac:
        change_mac(options.interface, options.new_mac)
        current_mac = get_current_mac(options.interface)
        if current_mac == options.new_mac:
            print("[+] MAC address was successfully changed to: " + current_mac)
        else:
            print("[+] MAC address did not change.")
    else:
        print("The interface: " + options.interface + " does not have a MAC address, please select another interface.")

def mac_changer():
    options = get_arguments()
    current_mac = get_current_mac(options.interface)
    print("Current Mac = " + str(current_mac))
    print_result(options, current_mac)

mac_changer()
