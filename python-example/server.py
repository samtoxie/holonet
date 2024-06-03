import socket
import traceback
from pprint import pprint
from threading import Thread


class HoloNetServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"HoloNet server running on {self.host}:{self.port}")
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_handler = Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def handle_client(self, client_socket):
        try:
            request = client_socket.recv(1024).decode('utf-8')
            print(f"Received request:\n{request}")
            response = self.handle_request(request)
        except Exception as e:
            response = "HLN/1.0 500 Internal Server Error\r\nContent-Type: text/plain\r\n\r\nAn error occurred."
            print(f"Error handling request: {e}")
            traceback.print_exc()
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

    def handle_request(self, request):
        lines = request.split('\r\n')
        if len(lines) < 1:
            return "HLN/1.0 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nMalformed request."

        request_line = lines[0].split()
        pprint(lines)
        print(request_line)
        print(len(request_line))
        if len(request_line) != 4:
            return "HLN/1.0 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nMalformed request line."

        protocol_name, method, resource, protocol_version = request_line
        headers = {}
        for line in lines[1:]:
            if line == '':
                break
            key, value = line.split(': ', 1)
            headers[key] = value

        body = '\r\n'.join(lines[lines.index('') + 1:]) if '' in lines else ''

        # Custom logic for handling requests
        if method == 'READ' and resource == '/':
            return "HLN/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\nWelcome to HoloNet!"
        else:
            return "HLN/1.0 404 Not Found\r\nContent-Type: text/plain\r\n\r\nResource not found."


if __name__ == '__main__':
    server = HoloNetServer()
    server.start()
