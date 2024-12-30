import socket  # noqa: F401
import threading
import os
def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221))
    while True:
        client_socket, client_address = server_socket.accept()
        # Create a new thread for each client
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, client_address)
        )
        client_thread.start()

def handle_client(client_socket, client_address):
    print(client_address)
    try:

        request = client_socket.recv(1024).decode("utf-8")
        if not request:
            return
        components = request.split("\r\n")
        method, path, httpversion = components[0].split(" ")
        path = path.lstrip("/")
        file_path = os.path.join("static", path)
        print(f"Path requested by the user is : {path}") 

        if os.path.exists(file_path):
            import mimetypes
            content_type, _ = mimetypes.guess_type(file_path) or "application/octet-stream"
            with open(file_path, "rb") as f:
                file_content = f.read()

            response = (
                f"HTTP/1.1 200 OK \r\n"
                "Content-Type : {content_type}\r\n"
                "Content-Length : {len(file_content)} \r\n"
                "\r\n"
            )
            client_socket.sendall(response.encode("utf-8"))
            client_socket.sendall(file_content)
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
