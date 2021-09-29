import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 65432))
while True:
    message_to_send = input("What would you like to send to the server? \n")
    client_socket.sendall(bytes(message_to_send, "utf-8"))

    received_message = client_socket.recv(1024)
    print("You received from the server this message:")
    print(repr(received_message))

