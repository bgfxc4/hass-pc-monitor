import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 5573)
sock.connect(server_address)
try:
    
    # Send data
    message = b'ATUH TestPassword'
    print('sending ' + str(message))
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    data = sock.recv(1048)
    amount_received += len(data)
    print('received "%s"' % data)

finally:
    print('closing socket')
    sock.close()