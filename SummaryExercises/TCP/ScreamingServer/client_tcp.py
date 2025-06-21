import socket as s

address = ("127.0.0.1", 8820)

sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.connect(address)
while True:
    message = input("Enter Your Message: ")
    sock.send(message.encode())
    data = sock.recv(1024).decode()
    print("The server sent " + data)
    if data == "bye!":
        break

sock.close()