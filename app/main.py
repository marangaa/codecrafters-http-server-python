import socket


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    client_socket, address = server_socket.accept()

    data = client_socket.recv(1024)

    request_str = data.decode("utf-8")
    request_lines = request_str.split("\r\n")

    request_line = request_lines[0]
    method, path, _ = request_line.split()

    if path == "/":
        response = f"HTTP/1.1 200 OK\r\n"
    else:
        response = f"HTTP/1.1 404 Not Found\r\n"

    client_socket.send(response)


if __name__ == "__main__":
    main()
