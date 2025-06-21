import socket as s

server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 8820))
server_socket.listen(1)
print( "Server is up and running" )
(client_socket, client_address) = server_socket.accept()
print("Client connected")

data = ""

while True:
    data = client_socket.recv(1024).decode()
    print( "Client sent: " + data)
    if data == "bye":
        client_socket.send("bye!".encode())
        client_socket.close()
        break
    client_socket.send(data.upper().encode())

server_socket.close()