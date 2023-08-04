import socket

def get_local_ip():
    try:
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(("8.8.8.8", 80))
        local_ip = temp_socket.getsockname()[0]
        temp_socket.close()
        return local_ip
    except Exception as e:
        print(f"Error getting local IP address: {e}")
        return None

def ask_save_option(file_name):
    option = input(f"A file with the name '{file_name}' already exists. Do you want to:\n1. Add the data to the existing file (A), or\n2. Replace the existing file (R)?\nYour choice (A/R): ").lower()
    return option

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = get_local_ip()
    if not server_ip:
        print("Failed to determine the local IP address. Exiting.")
        return

    server_port = 12345
    server_socket.bind((server_ip, server_port))

    server_socket.listen(5)
    print(f"Server is listening on {server_ip}:{server_port}")

    data_received = []	

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")

            data = client_socket.recv(1024).decode('utf-8')	
            print(f"Received data from client: {data}")

            data_received.append(data)

            client_socket.close()

    except KeyboardInterrupt:
        print(f"KeyboardInterrupt detected. Closing the server.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()