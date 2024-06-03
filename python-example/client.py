import socket

class HoloNetClient:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_request(self, method, resource, body=''):
        request = f"HLN {method} {resource} HLN/1.0\r\nContent-Length: {len(body)}\r\n\r\n{body}"
        print(request.encode('utf-8'))
        self.client_socket.connect((self.host, self.port))
        self.client_socket.sendall(request.encode('utf-8'))
        response = self.client_socket.recv(1024).decode('utf-8')
        print(f"Received response:\n{response}")
        self.client_socket.close()

if __name__ == '__main__':
    client = HoloNetClient()
    client.send_request('READ', '/')
