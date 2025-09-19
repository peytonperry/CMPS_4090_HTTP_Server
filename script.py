import socket
import os

#NOTE: I had some odd issues with it sometimes not serving the file. It may have just been a Brave thing OR my certificates but im not sure.
#IF it serves a blank page just restart the server and try again. I spent too much time trying to solve and I just couldn't figure out the problem.

#getting the file type so we can also serve css
def get_mime_type(filename):
    if filename.endswith('.html') or filename.endswith('.htm'):
        return 'text/html'
    elif filename.endswith('.css'):
        return 'text/css'
    else:
        return 'text/plain'

#this is all the request handling. We get a request and decode
def handle_request(client_socket):
    request = client_socket.recv(1024).decode('utf-8')


    first_line = request.split('\n')[0]
    url = first_line.split()[1]
    #if in our decode we see that it is requesting a url ending in '/' we send the client our index.html
    if url == '/':
        filename = 'index.html'
    else:
        filename = url[1:]
    #begin parsing the file selected
    try:
        with open(filename, 'rb') as f:
            content = f.read()
        #get the file type
        content_type = get_mime_type(filename)

        #coded responses to send with our file
        response = f"HTTP/1.0 200 OK\r\n"
        response += f"Content-Type: {content_type}\r\n"
        response += f"Content-Length: {len(content)}\r\n"
        response += "\r\n"
        #finally encoding and sending the content of our file.
        client_socket.send(response.encode('utf-8'))
        client_socket.send(content)
        #logging that we successfully sent the file
        print(f"Served: {filename}")
    #error handling
    except FileNotFoundError:
        error_message = "File Not Found"
        response = f"HTTP/1.0 404 Not Found\r\n"
        response += f"Content-Type: text/plain\r\n"
        response += f"Content-Length: {len(error_message)}\r\n"
        response += "\r\n"
        response += error_message

        client_socket.send(response.encode('utf-8'))
        print(f"404: {filename}")

    client_socket.close()


def start_server():
    #setting the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #bind and listen to port
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)
    #give the link to our server so you can view our beautiful html
    print("Server running on http://localhost:8080")

    try:
        while True:
            #while loop so we stay connected and logging our connected device
            client_socket, address = server_socket.accept()
            print(f"Connection from {address}")
            #serve the file
            handle_request(client_socket)

    except KeyboardInterrupt:
        print("\nServer stopped")
    finally:
        server_socket.close()
#run tha serva
if __name__ == '__main__':
    start_server()