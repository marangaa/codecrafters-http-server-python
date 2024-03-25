import socket
import os
from argparse import ArgumentParser
import threading


def main():
    parser = ArgumentParser()
    parser.add_argument("--directory", type=str, default=None)
    args = parser.parse_args()
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_socket, address_info = server_socket.accept()  # wait for client
        threading.Thread(
            target=handle_request, args=(client_socket, address_info, args.directory)
        ).start()


def handle_request(client_socket, address_info, directory):
    with client_socket:
        # status = "HTTP/1.1 200 OK\r\n\r\n"
        request = client_socket.recv(1024).decode("utf-8")
        request = request.split("\r\n")

        method = request[0].split()[0]
        data_path = request[0].split()[1]
        if data_path == "/":
            status = "HTTP/1.1 200 OK\r\n\r\n"
        elif data_path.startswith("/echo"):
            random_string = data_path.split("/echo/")[1]
            status = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                f"Content-Length: {len(random_string)}\r\n\r\n"
                f"{random_string}"
            )
        elif data_path.startswith("/user-agent"):
            user_agent_header = request[2]
            user_agent_data = user_agent_header.split("User-Agent: ")[1]
            status = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                f"Content-Length: {len(user_agent_data)}\r\n\r\n"
                f"{user_agent_data}"
            )
        elif data_path.startswith("/files"):
            if directory:
                filename = data_path.split("/files/")[1]
                file = os.path.join(directory, filename)
                if method == "GET":
                    if os.path.exists(file) and os.path.isfile(file):
                        with open(file, "rb") as f:
                            file_data = f.read()
                        status = (
                            "HTTP/1.1 200 OK\r\n"
                            "Content-Type: application/octet-stream\r\n"
                            f"Content-Length: {len(file_data)}\r\n\r\n"
                            f"{file_data.decode()}"
                        )
                    else:
                        status = "HTTP/1.1 404 Not Found\r\n\r\n"
                elif method == "POST":
                    file_data = request[-1]
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    with open(file, "wb") as f:
                        f.write(file_data.encode())

                    status = "HTTP/1.1 201 OK\r\n\r\n"
        else:
            status = "HTTP/1.1 404 Not Found\r\n\r\n"
            # status = status.encode("utf-8")
        client_socket.send(status.encode())


if __name__ == "__main__":
    main()
