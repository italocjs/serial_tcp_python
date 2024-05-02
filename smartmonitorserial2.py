import socket
import sys
import time
import threading
import argparse
from datetime import datetime

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

def log_data(data, host, port, log_filename):
    """Log the given data to a specified file."""
    # Open the file in append mode and write the data
    with open(log_filename, 'a') as file:
        file.write(data + '\n')

def send_data(sock, host, port, log_filename):
    """Function to send data to the server based on user input."""
    try:
        while True:
            user_input = input()
            message = user_input + '\r\n'
            sock.sendall(message.encode('utf-8'))
            log_data(user_input, host, port, log_filename)  # Log the sent data
    except Exception as e:
        print(f"Error sending data: {e}")

def main():
    parser = argparse.ArgumentParser(description="Connect to a server and optionally display data in HEX format.")
    parser.add_argument('host', type=str, help="The IP address of the server")
    parser.add_argument('port', type=int, help="The port number of the server")
    parser.add_argument('--mode', type=str, help="Display mode: HEX for hexadecimal display, anything else for string display", default="")
    parser.add_argument('--log', nargs='?', const='AUTO', type=str, help="Optional log file name or auto-generate if not specified")

    args = parser.parse_args()

    host = args.host
    port = args.port
    mode = args.mode
    # Determine log filename at the start
    if args.log is None:
        log_filename = None  # No logging
    elif args.log == 'AUTO':
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"{host}_{port}_{timestamp}.txt"
    else:
        log_filename = args.log

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((host, port))
            sock.setblocking(0)
            print(f'Connected to {host}:{port}')
            
            send_thread = threading.Thread(target=send_data, args=(sock, host, port, log_filename))
            send_thread.daemon = True
            send_thread.start()
            
            while True:
                try:
                    data = sock.recv(1024)
                    if data:
                        display_data(data, mode)  # Pass the mode to the display function
                        if log_filename:  # Check if logging is enabled
                            log_data(data.decode('utf-8', errors='ignore'), host, port, log_filename)  # Log the received data
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
