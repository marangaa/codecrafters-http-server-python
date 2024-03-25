import socket
import sys
import os
import threading


def parse_headers(request):
    stringdata = request.decode("utf-8")
    start_index = stringdata.find("GET ") + len("GET ")
    end_index = stringdata.find(" HTTP")
    address = stringdata[start_index:end_index]

    if address.startswith("/echo/"):
        res_string = address[6:]
        content_length = len(res_string)
        res = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{res_string}".encode(
            "utf-8"
        )
    elif address.startswith("/files/"):
        filename = address[7:]
        if sys.argv[1] == "--directory":
            path = sys.argv[2] + filename
            if os.path.isfile(path):
                with open(path, "r") as file:
                    res_string = file.read()
                    content_length = len(res_string)
                    res = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {content_length}\r\n\r\n{res_string}".encode(
                        "utf-8"
                    )
            else:
                res = b"HTTP/1.1 404 Not Found\r\n\r\n"
    elif address == "/user-agent":
        res_string = [
            data[12:]
            for data in stringdata.split("\r\n")
            if data.startswith("User-Agent: ")
        ][0]
        content_length = len(res_string)
        res = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n{res_string}".encode(
            "utf-8"
        )
    elif address == "/":
        res = b"HTTP/1.1 200 OK\r\n\r\n"
    else:
        res = b"HTTP/1.1 404 Not Found\r\n\r\n"
    return res


def handle_client(conn):
    req = conn.recv(1024)
    res = parse_headers(req)
    conn.send(res)
    conn.close()


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        conn, _ = server_socket.accept()  # wait for client
        threading.Thread(target=handle_client, args=(conn,)).start()


if __name__ == "__main__":
    main()
