import socket
import sys
import time
import threading
import argparse  # Import the argparse module

def display_hex(data):
    """Display the given data in hexadecimal format."""
    hex_data = data.hex()
    hex_str = ' '.join(hex_data[i:i+2] for i in range(0, len(hex_data), 2))
    print(hex_str)

def display_data(data, mode):
    """Display the given data based on the specified mode."""
    if mode.upper() == 'HEX':
        display_hex(data)
    else:
        try:
            string_repr = data.decode('utf-8')
        except UnicodeDecodeError:
            string_repr = '<binary data>'
        print(string_repr)

def send_data(sock):
    """Function to send data to the server based on user input."""
    try:
        while True:
            user_input = input()
            message = user_input + '\r\n'
            sock.sendall(message.encode('utf-8'))
    except Exception as e:
        print(f"Error sending data: {e}")

def main():
    parser = argparse.ArgumentParser(description="Connect to a server and optionally display data in HEX format.")
    parser.add_argument('host', type=str, help="The IP address of the server")
    parser.add_argument('port', type=int, help="The port number of the server")
    parser.add_argument('--mode', type=str, help="Display mode: HEX for hexadecimal display, anything else for string display", default="")

    args = parser.parse_args()

    host = args.host
    port = args.port
    mode = args.mode  # Retrieve the mode argument

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((host, port))
            sock.setblocking(0)
            print(f'Connected to {host}:{port}')
            
            send_thread = threading.Thread(target=send_data, args=(sock,))
            send_thread.daemon = True
            send_thread.start()
            
            while True:
                try:
                    data = sock.recv(1024)
                    if data:
                        display_data(data, mode)  # Pass the mode to the display function
                    else:
                        time.sleep(0.1)
                except BlockingIOError:
                    time.sleep(0.1)
                except KeyboardInterrupt:
                    print('\nDisconnected from server.')
                    break
        except KeyboardInterrupt:
            print('\nDisconnected from server.')
        except Exception as e:
            print(f'An error occurred: {e}', file=sys.stderr)

if __name__ == '__main__':
    main()
