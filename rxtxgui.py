import socket
import threading
import curses

def setup_curses():
    """Initializes the curses environment."""
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    return stdscr

def teardown_curses(stdscr):
    """Restores the terminal to its original state."""
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

def send_data(sock, win):
    """Function to send data to the server based on user input."""
    while True:
        win.clear()
        win.addstr("Message: ")
        win.refresh()
        message = win.getstr().decode('utf-8') + '\r\n'
        sock.sendall(message.encode('utf-8'))

def receive_data(sock, stdscr):
    """Function to receive and display incoming data."""
    stdscr.nodelay(True)  # Make getch non-blocking
    while True:
        try:
            data = sock.recv(1024)
            if data:
                stdscr.addstr(data.decode('utf-8'))
                stdscr.refresh()
        except socket.error:
            pass

def main(stdscr, host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.setblocking(0)

    # Creating a new window for input at the bottom of the terminal
    input_win = curses.newwin(1, curses.COLS, curses.LINES-1, 0)

    # Starting threads for sending and receiving data
    send_thread = threading.Thread(target=send_data, args=(sock, input_win,))
    receive_thread = threading.Thread(target=receive_data, args=(sock, stdscr,))

    send_thread.daemon = True
    receive_thread.daemon = True

    send_thread.start()
    receive_thread.start()

    while True:
        # Main loop to keep the interface running, exit on Ctrl+C or window close
        pass

if __name__ == '__main__':
    host = '192.168.1.11'
    port = 8880
    stdscr = setup_curses()
    try:
        main(stdscr, host, port)
    except KeyboardInterrupt:
        pass
    finally:
        teardown_curses(stdscr)
