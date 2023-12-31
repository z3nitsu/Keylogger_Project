import socket
import os
import threading
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

save_option = None

def ask_save_option(file_name):
    global save_option
    if save_option is None:
        if os.path.isfile(file_name):
            option = input(f"A file with the name '{file_name}' already exists. Do you want to:\n1. Add the data to the existing file (A), or\n2. Replace the existing file (R)?\nYour choice (A/R): ").lower()
            if option not in ('a', 'r'):
                print("Invalid choice. Defaulting to 'A' (Add).")
                option = 'a'
        else:
            print(f"File '{file_name}' does not exist. Creating a new file.")
            option = 'a'
        save_option = option
    return save_option

def handle_client(client_socket):
    data_received = []
    file_name = 'received_data.txt'

    try:
        file_created = False

        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            print(f"Received data from client: {data}")

            if data.strip().lower() == 'exit':
                print("Exit command received.")
                break

            data_received.append(data)

            if not file_created:
                option = ask_save_option(file_name)
                if option == 'a':
                    with open(file_name, 'a') as file:
                        file.write(data + '\n')
                elif option == 'r':
                    with open(file_name, 'w') as file:
                        file.write(data + '\n')
                file_created = True
            else:
                with open(file_name, 'a') as file:
                    file.write(data + '\n')

    except Exception as e:
        print(f"Error handling client data: {e}")
    finally:
        client_socket.close()

def start_server():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = get_local_ip()
    if not server_ip:
        print("Failed to determine the local IP address. Exiting.")
        return

    server_port = 12345
    server_socket.bind((server_ip, server_port))

    server_socket.listen(5)
    print(f"Server is listening on {server_ip}:{server_port}")
    
def main():
    start_server()
    try:
        while True:
            # Accept a connection from a client
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")

            # Create a separate thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt detected. Closing the server.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()