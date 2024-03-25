import socket

import threading


def process_client(client_socket_object: socket.socket):
    data = client_socket_object.recv(1024).decode("utf-8")
    separate_lines = data.split("\r\n")
    path = separate_lines[0].split()[1]

    if path == "/":
        response = b"HTTP/1.1 200 OK\r\n\r\n"
    elif path.startswith("/echo/"):
        text = path.split("/echo/")[1]
        to_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(text)}\r\n\r\n{text}"
        response = to_response.encode()
    elif path.startswith("/user-agent"):
        text = separate_lines[2].split()[1]
        to_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(text)}\r\n\r\n{text}"
        response = to_response.encode()
    else:
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"

    client_socket_object.send(response)


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        (
            client_socket_object,
            address_info_port,
        ) = server_socket.accept()  # wait for client

        threading.Thread(target=process_client, args=(client_socket_object,)).start()


if __name__ == "__main__":
    main()
