import socket as s

client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
print("Created Socket")
client_socket.connect(("127.0.0.1", 9000))
print("Connected To Server")

while True:
    message = input("Enter Command: ")
    client_socket.send(message.encode())
    response = client_socket.recv(1024).decode()
    print(response)
    if response == "Bye!":
        break

client_socket.close()