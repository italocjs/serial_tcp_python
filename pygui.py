import PySimpleGUI as sg
import socket
import threading

# TCP server address and port
HOST = '192.168.1.11'
PORT = 8880

def tcp_client(window):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.setblocking(False)
        
        while True:
            event, values = window.read(timeout=10)
            if event == sg.WIN_CLOSED:
                break
            elif event == 'Send':
                message = values['-IN-'] + '\r\n'
                sock.sendall(message.encode('utf-8'))
                window['-IN-'].update('')
            
            try:
                while True:  # Keep reading until there's no more data
                    data = sock.recv(1024)
                    if not data:
                        break  # No more data received
                    window['-OUT-'].update(values['-OUT-'] + data.decode('utf-8') + '\n')
            except BlockingIOError:
                continue  # No data available to read


# Define the window layout
layout = [
    [sg.Text('Enter your message:')],
    [sg.InputText(key='-IN-')],
    [sg.Button('Send'), sg.Button('Exit')],
    [sg.Text('Received messages:')],
    [sg.Multiline(size=(45, 10), key='-OUT-', autoscroll=True, disabled=True)],
]

# Create the window
window = sg.Window('TCP Client GUI', layout)

# Start the TCP client thread
threading.Thread(target=tcp_client, args=(window,), daemon=True).start()

# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

window.close()
