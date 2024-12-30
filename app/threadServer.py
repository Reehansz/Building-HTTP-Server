import threading
from socket import create_server

# Function to handle each client connection
def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    try:
        request = client_socket.recv(1024).decode('utf-8')
        print("Request:\n", request)

        # Parse request
        lines = request.splitlines()
        request_line = lines[0]
        method, path, http_version = request_line.split()

        # Create a response
        body = f"""
        <html>
        <body>
            <h1>Welcome to the Multi-Threaded Server</h1>
            <p>You requested: {path}</p>
        </body>
        </html>
        """
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(body)}\r\n"
            "\r\n"
            f"{body}"
        )

        client_socket.sendall(response.encode('utf-8'))
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()

# Main server loop
def start_server():
    server_socket = create_server(("127.0.0.1", 8080))
    print("Server is running on http://127.0.0.1:8080")

    while True:
        client_socket, client_address = server_socket.accept()
        # Create a new thread for each client
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, client_address)
        )
        client_thread.start()

# Start the server
start_server()
