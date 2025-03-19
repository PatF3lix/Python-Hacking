import scapy.all as scapy
import subprocess
import optparse
import re

# Must be run with sudo privileges: sudo python network_scanner.py

# def scan(ip):
#     scapy.arping(ip)

def get_ip_from_user_input():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--ip", dest="current_ip", help="192.168.0.1/24")
    (options, arguments) = parser.parse_args()
    if not options.current_ip:
        parser.error("Please specify a valid IP range with /16, or /24. use --help for more info")

    return options.current_ip

def validate_ip_with_subnet(ip_with_subnet):
    # Regular expression to match the pattern "xxx.xxx.xxx.xxx/n"
    pattern = r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/(\d{1,2})$"
    valid_ip_with_subnet =  False
    
    match = re.match(pattern, ip_with_subnet)
    if match:
        ip = match.group(1)
        subnet = match.group(2)
        
        if is_valid_ip(ip) and is_valid_subnet(subnet):
            valid_ip_with_subnet = True

    return valid_ip_with_subnet, ip, subnet

def is_valid_ip(ip):
    base_parts = ip.split(".")
    valid_ip = True
    for ip in base_parts:
        if 0 < int(ip) < 255:
            continue
        else:
            valid_ip = False
            break

    return valid_ip

def is_valid_subnet(subnet):
    valid_subnet = False
    if subnet == "16" or subnet == "24":
        valid_subnet = True
    return valid_subnet


def get_ip_range_endpoint(ip, subnet):
    ip_range_endpoint = ""

    if subnet == "16":
        ip_range_endpoint = f"{ip[0]}.{ip[1]}.255.255"
    if subnet == "24":
        ip_range_endpoint = f"{ip[0]}.{ip[1]}.{ip[2]}.255"
    return ip_range_endpoint

def incrementing_ip(ip_range, subnet):

    if int(ip_range[3]) < 255:
        ip_range[3] = str(int(ip_range[3]) + 1)
    
    if subnet == "16" and int(ip_range[3]) == 255:
        if int(ip_range[2]) <= 254:
            ip_range[3] = "1"
            ip_range[2] = str(int(ip_range[2]) + 1)
        else:
            ip_range[3] = "255"

    return f"{ip_range[0]}.{ip_range[1]}.{ip_range[2]}.{ip_range[3]}"

def scan(ip):
    # Create ARP request to find the MAC address of the given IP
    arp_request = scapy.ARP(pdst=ip)
    # arp_request.show()
    
    # Create Ethernet frame with broadcast destination MAC address
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # broadcast.show()

    # Combine the Ethernet frame and ARP request
    arp_request_broadcast = broadcast/arp_request
    # arp_request_broadcast.show()

    # returns answered and unanswered packets, timeout is how long 
    answered_list = scapy.srp(arp_request_broadcast, timeout = 1, verbose = False)[0]

    answer = ()

    for element in answered_list:
        ip = element[1].psrc
        mac = element[1].hwsrc
        answer = (ip, mac)
    
    return answer

def print_scan_results(answered_list):
    print("\nIP\t\t\t\tMAC Adress")
    print("-------------------------------------------------------------")
    for ip, mac in answered_list:
        print(f"{ip}\t\t\t{mac}")

def print_valid_input(current_ip, subnet):
    print(f"Valid IP: {current_ip}")
    print(f"Valid Subnet Mask: /{subnet}")
    print("-------------------------------------------------------------")

def network_scanner():

    ip_with_subnet = get_ip_from_user_input()
    valid_ip_and_subnet, ip, subnet = validate_ip_with_subnet(ip_with_subnet)

    if valid_ip_and_subnet:
        current_ip = ip
        ip_range = ip.split(".")
        subnet_endpoint = get_ip_range_endpoint(ip_range, subnet)
        answered_list = []
        print_valid_input(current_ip, subnet)
        # change this literal "192.168.60.10" for subnet_endpoint when you want to scan the whole subnet
        while current_ip != "192.168.60.10": 
            print(f"scanning: {current_ip}/{subnet}")
            new_answer = scan(current_ip)
            if new_answer:
                answered_list.append(new_answer)
            current_ip = incrementing_ip(ip_range, subnet)
        print_scan_results(answered_list)
    else:
        print("Invalid format. Please provide the IP in the format '192.168.0.1/24'.")

network_scanner()