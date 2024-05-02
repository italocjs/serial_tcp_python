import socket
import sys
import time
import threading

def display_hex(data):
    """Display the given data in hexadecimal format."""
    hex_data = data.hex()
    hex_str = ' '.join(hex_data[i:i+2] for i in range(0, len(hex_data), 2))
    print(hex_str)

def display_data(data):
    """Display the given data as both hex and interpreted string."""
    hex_data = data.hex()
    hex_str = ' '.join(hex_data[i:i+2] for i in range(0, len(hex_data), 2))

    try:
        string_repr = data.decode('utf-8')
    except UnicodeDecodeError:
        string_repr = '<binary data>'

    # print("Hexadecimal Representation:")
    # print(hex_str)
    # print("\nInterpreted String (with control characters):")
    print(string_repr)
    # print("\n---------------------------------------------")

def send_data(sock):
    """Function to send data to the server based on user input."""
    try:
        while True:
            # Wait for user input
            user_input = input()
            # Append '\r\n' to the user input to ensure proper message termination
            message = user_input + '\r\n'
            # Send input as encoded bytes
            sock.sendall(message.encode('utf-8'))
    except Exception as e:
        print(f"Error sending data: {e}")


def main():
    host = '192.168.1.11'
    port = 8880

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((host, port))
            sock.setblocking(0)  # Set socket to non-blocking mode
            print(f'Connected to {host}:{port}')
            
            # Start a new thread for sending data
            send_thread = threading.Thread(target=send_data, args=(sock,))
            send_thread.daemon = True  # Daemonize thread
            send_thread.start()
            
            while True:
                try:
                    data = sock.recv(1024)
                    if data:
                        display_data(data)
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
