import scapy.all as scapy

def sniff(interface):
    scapy.sniff(iface= interface, store= False, prn= process_sniffed_packet, filter= "")

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


def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc
            if real_mac != response_mac:
                print("[+] You are under ARP attack!")
            # print(packet.show())
        except IndexError:
            pass

def packet_sniffer():
    try:
        while True:
            sniff("eth0")
    except KeyboardInterrupt:
        print("Quiting Packet Sniffer")

packet_sniffer()