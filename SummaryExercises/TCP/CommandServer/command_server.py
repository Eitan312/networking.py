import socket as s
import time
import random

__ALLOWED_COMMANDS = ["QUIT", "RAND", "TIME","NAME"]
__NAME = "Eitan's Command Server"

print("Creating Socket...")
server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
print("Socket Created Successfully")
print("Binding Socket...")
server_socket.bind(("127.0.0.1", 9000))
print("Bound Socket")
server_socket.listen(1)
print("Server Up And Running")
client_socket, client_address = server_socket.accept()
print("Connection Established, Initiating Conversation")

while True:
    data = client_socket.recv(1024).decode()

    if data.upper() not in __ALLOWED_COMMANDS:
        client_socket.send("Command Not Found".encode())
    elif data.upper() == "NAME":
        client_socket.send(__NAME.encode())
    elif data.upper() == "TIME":
        localTime = time.localtime(time.time())
        client_socket.send(time.strftime("%a, %d %b %Y %H:%M:%S",localTime).encode())
    elif data.upper() == "RAND":
        randomNumber = random.randint(1, 10)
        client_socket.send(str(randomNumber).encode())
    elif data.upper() == "QUIT":
        client_socket.send("Bye!".encode())
        client_socket.close()
        break

print("Closing Server...")
server_socket.close()
print("Server Is Down")