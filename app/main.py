import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket_object, address_info_port = server_socket.accept()  # wait for client
    data = client_socket_object.recv(1024).decode("utf-8")
    separate_lines = data.split("\r\n")
    path = separate_lines[0].split()[1]
    if path == "/":
        response = b"HTTP/1.1 200 OK\r\n\r\n"
    else:
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"
    client_socket_object.send(response)
