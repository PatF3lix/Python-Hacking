import socket

# Socket documentation
# https://docs.python.org/2/library/socket.html

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("192.168.60.2", 4444))

connection.send(b"\n[+] Connection established")

# 
received_data = connection.recv(1024)
print(str(received_data))

connection.close()