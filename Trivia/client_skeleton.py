import socket as s
import Trivia.chatlib_skeleton as chatlib  # To use chatlib functions or consts, use cha

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Parameters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    msg = chatlib.build_message(code, data)
    conn.send(msg.encode())


def recv_message_and_parse(conn):
    """
    Receives a new message from given socket,
    then parses the message using chatlib.
    Parameters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occurred, will return None, None
    """
    full_msg = conn.recv(1024).decode()
    cmd, data = chatlib.parse_message(full_msg)
    return cmd, data


def connect():
    trivia_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    trivia_socket.connect((SERVER_IP, SERVER_PORT))
    return trivia_socket


def error_and_exit(error_msg):
    exit(error_msg)


def login(conn):
    username = input("Please enter username: \n")
    password = input("Please enter password: \n")
    print("Checking...")
    while True:
        data = chatlib.join_data([username, password])
        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], data)
        result, data = recv_message_and_parse(conn)
        if result == "LOGIN_OK":
            break
        print("Incorrect Credentials, Please Enter Again.")
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")
        print("Checking...")

    print("Login Ok!")


def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")


def main():
    trivia_socket = connect()
    login(trivia_socket)
    logout(trivia_socket)


if __name__ == '__main__':
    main()
