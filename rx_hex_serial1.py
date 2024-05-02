import socket
import sys
import time

def display_hex(data):
    """Display the given data in hexadecimal format."""
    hex_data = data.hex()
    hex_str = ' '.join(hex_data[i:i+2] for i in range(0, len(hex_data), 2))
    print(hex_str)

def display_data(data, mode):
    """Display the given data as both hex and interpreted string."""
    # Convert and format the data as hexadecimal
    hex_data = data.hex()
    hex_str = ' '.join(hex_data[i:i+2] for i in range(0, len(hex_data), 2))

    # Attempt to decode the data to a string for printing
    try:
        string_repr = data.decode('utf-8')
    except UnicodeDecodeError:
        string_repr = '<binary data>'

    print("Hexadecimal Representation:")
    print(hex_str)
    print("\nInterpreted String (with control characters):")
    print(string_repr)
    print("\n---------------------------------------------")

def main():
    host = '192.168.1.11'
    port = 8880

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((host, port))
            sock.setblocking(0)  # Set socket to non-blocking mode
            print(f'Connected to {host}:{port}')
            
            while True:
                try:
                    data = sock.recv(1024)
                    if data:
                        # display_hex(data)
                        display_data(data)
                    else:
                        # Sleep briefly to avoid a tight loop when no data is available
                        time.sleep(0.1)
                except BlockingIOError:
                    # No data available, sleep briefly to avoid a tight loop
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
