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
        method, path, httpversion = components[0].split()
        print(f"Path requested by the user is : {path}") 

        headers = {}
        for header in components[1:]:
            if header:
                key, value = header.split(": ", 1)
                headers[key.strip()] = value.strip()
        
        if path == "/":
            body = f'''<html>
                        <body>  
                            <h1>Hey welcome to the page, this is me Reehan, path requested by you is {path}, method is {method}</h1>
                            <p><a href="/about">About</a></p>
                            <p><a href="/contact">Contact</a></p>
                            <p><a href="/headers">Headers</a></p>
                        </body>
                        </html>'''
        # elif path == "/hello":
        #     response = ("HTTP/1.1 200 OK\r\n"
        #                 "Content-Type: text/html\r\n\r\n"
        #                 "<html><body><h1>Welcome to the hello page </h1></body></html\r\n")
        # else:
        #     response = ("HTTP/1.1 404 Not Found\r\n\r\n"
        #                 "<html> <style> body{text-align: center; font-size : 5rem}"
        #                 "h1,h3{margin-bottom: 0px;"
        #                 "margin-top: 0px;} </style><body><h3>Page not found</h3><br><h1>404</h1></body></html>\r\n")
        
        elif path == "/headers":
            body = "<html><body><h1>Headers Received</h1><ul>"
            for key, value in headers.items():
                body += f"<li>{key}: {value}</li>"
            body += "</ul></body></html>"
        elif path == "/about":
            body = "<h1>About Us</h1><p>This is the about page.</p>"

        elif path == "/contact":
            body = "<h1>Contact Us</h1><p>Email us at contact@example.com</p>"

        else :
            body = "<html><body style='text-align : center'><h3>Page not found</h3><br><h1>404</h1></body></html>"
        
        response = ("HTTP/1.1 200 OK \r\n"
                    "Content-Type: text/html\r\n"
                    f"Content-Length: {len(body)}\r\n\r\n"
                    f"{body}\r\n")
        client_socket.sendall(response.encode("utf-8"))
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
