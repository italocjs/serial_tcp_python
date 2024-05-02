### README for SmartMonitorSerial1

#### Overview
[smartmonitorserial1.py]is a Python script designed to connect to a TCP server and display incoming data either as a string or in hexadecimal format. It supports user input to send data back to the server. This tool is useful for debugging and monitoring data communications over TCP.

#### Requirements
- Python 3.x
- A TCP server to connect to

#### Installation
No specific installation steps required other than having Python installed. Simply download [smartmonitorserial1.py] to your local machine.

#### Usage
To use [smartmonitorserial1.py] you need to specify the host IP address and the port number of the TCP server you want to connect to. Optionally, you can specify the display mode for incoming data.

##### Basic Commands
- **Connect to a server**:  
  ```bash
  python .\smartmonitorserial1.py <host> <port>
  ```
  Replace `<host>` with the IP address of the server and `<port>` with the port number.

- **Connect to a server with hexadecimal display**:  
  ```bash
  python .\smartmonitorserial1.py <host> <port> --mode HEX
  ```
  This command will display incoming data in hexadecimal format.

##### Examples
- Connect to a server at IP `192.168.1.11` on port `8880`:
  ```bash
  python .\smartmonitorserial1.py 192.168.1.11 8880
  ```
- Connect to the same server with data displayed in hexadecimal format:
  ```bash
  python .\smartmonitorserial1.py 192.168.1.11 8880 --mode HEX
  ```

#### Supported Commands
- **Sending Data**: Once connected, type your message and press Enter to send it to the server.
- **Exit**: Use `Ctrl+C` to safely disconnect from the server and close the application.

#### Logging
Currently, the script does not support logging to a file directly. To log the session, you can redirect the output to a file using:
```bash
python .\smartmonitorserial1.py <host> <port> > log.txt
```
For hexadecimal mode:
```bash
python .\smartmonitorserial1.py <host> <port> --mode HEX > log.txt
```

#### Troubleshooting
- **Connection Issues**: Ensure the server IP address and port are correct and that the server is accepting connections.
- **Display Issues**: If the data does not display correctly, try switching the display mode or check the data encoding.

This script is a powerful tool for real-time data monitoring and testing server communications. Adjust the host and port parameters according to your server's configuration.