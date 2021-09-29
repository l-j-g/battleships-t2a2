import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
with server_socket as s:
    s.bind(("127.0.0.1", 65432))
    s.listen()
    print(f"Listening for incoming connection on port 65432")

    connection, address = s.accept()
print(f"Connected by {address}")

while True:
    data = connection.recv(1024)
    print(f"recieved: {data}")
    if not data:
        break
    connection.sendall(data.upper())

server_socket.close()