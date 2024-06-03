import base64
import json

import gnupg

import HoloLib
import socket
import traceback
from threading import Thread


class HoloException(Exception):
    def __init__(self, msg, status, keyword):
        self.msg = msg
        self.status = status
        self.keyword = keyword


class HoloNetServer:
    def __init__(self, host='localhost', port=8080):
        self.gpg_key_id = "70F8FB59BEF4D9B4F1B1182A13ABF5B8A9E3A1F7"
        self.gpg = gnupg.GPG()
        self.gpg_key_b64 = base64.b64encode(self.gpg.export_keys(self.gpg_key_id).encode()).decode()
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

    def decrypt_request(self, request):
        return HoloLib.decrypt_and_verify(request, gpg=self.gpg)

    def handle_client(self, client_socket):
        try:
            request = client_socket.recv(4096).decode()

            if "HLN/0.1" not in request:
                request = self.decrypt_request(request)

            print(f"Received request:\n{request}")
            try:
                response, client_key_id = self.handle_request(request)
                response = HoloLib.encrypt_and_sign(response, client_key_id, self.gpg_key_id, gpg=self.gpg)
            except HoloException as e:
                headers = {'Content-Type': 'text/plain'}
                response = HoloLib.create_formatted_response(e.status, e.keyword, self.gpg_key_b64, headers, e.msg)
        except Exception as e:
            headers = {'Content-Type': 'text/plain'}
            response = HoloLib.create_formatted_response(500, "INTERNAL_ERROR", self.gpg_key_b64, headers,
                                                         "Undefined error in the server!")
            print(f"Error handling request: {e}")
            traceback.print_exc()

        client_socket.sendall(response.encode())
        client_socket.close()

    def parse_holoheader(self, line):
        parts = line.split(' ')

        if len(parts) != 3:
            raise HoloException(f"Malformed HoloHeader.", 400, "BAD_REQUEST")

        protocol, method, resource = parts

        if protocol != "HLN/0.1":
            raise HoloException(f"Incorrect protocol, I only support HLN/0.1.", 400, "BAD_REQUEST")

        if method != "READ" and method != "WRITE":
            raise HoloException(f"Unsupported method.", 400, "BAD_REQUEST")

        return method, resource

    def parse_headers(self, headers_raw: str):
        headers_splitted = headers_raw.split('\n')

        headers = {}

        for header in headers_splitted:
            if ":" not in header:
                continue
            header_split = header.split(':')
            key = header_split[0].strip()
            val = header_split[1].strip()
            headers[key] = val

        return headers

    def add_client_key(self, client_key_b64):
        try:
            client_key = base64.b64decode(client_key_b64)
            result = self.gpg.import_keys(client_key)
            return result.fingerprints[0]
        except Exception:
            raise HoloException(f"Invalid Public Key.", 400, "BAD_REQUEST")

    def handle_request(self, request):
        sections = request.split('\n\n')

        if len(sections) != 4:
            raise HoloException(f"Incorrect number of sections, expected 4 but got {len(sections)}.", 400,
                                "BAD_REQUEST")

        holoheader, client_key_b64, request_headers, body = sections

        method, resource = self.parse_holoheader(holoheader)
        req_headers = self.parse_headers(request_headers)
        client_key_id = self.add_client_key(client_key_b64)

        # Custom logic for handling requests
        if method == 'READ' and resource == '/':
            headers = {'Content-Type': 'text/plain'}
            return HoloLib.create_formatted_response(200, "OK", self.gpg_key_b64, headers,
                                                     "Welcome to HoloNet!"), client_key_id
        elif method == 'READ' and resource == '/hello-world':
            headers = {'Content-Type': 'text/plain'}
            return HoloLib.create_formatted_response(200, "OK", self.gpg_key_b64, headers,
                                                     "Hello World!"), client_key_id
        elif method == 'READ' and resource == '/server-key':
            headers = {'Content-Type': 'text/json'}
            body = {
                "message": "This is an unsecure exchange. It works, but could theoretically still allow a MITM-attack. Instead please retrieve the server key from a trusted root server preprogrammed into your client.",
                "key": self.gpg_key_b64
            }
            return HoloLib.create_formatted_response(200, "OK", self.gpg_key_b64, headers,
                                                     json.dumps(body)), client_key_id
        else:
            return HoloLib.create_formatted_response(404, "NOT_FOUND", self.gpg_key_b64, {},
                                                     "Resource not found."), client_key_id


if __name__ == '__main__':
    server = HoloNetServer()
    server.start()
