import base64
import json
import socket

import gnupg

import HoloLib


class HoloNetClient:
    def __init__(self, host='localhost', port=8080):
        self.gpg_key_id = "90BDDDBB863C2E4459B3FBAEBB319F560715AF10"
        self.gpg = gnupg.GPG()
        self.gpg_key_b64 = base64.b64encode(self.gpg.export_keys(self.gpg_key_id).encode()).decode()
        self.host = host
        self.port = port
        self.server_key_ids = {}

    def parse_holoheader(self, line):
        parts = line.split(' ')

        if len(parts) != 3:
            raise Exception(f"Malformed HoloHeader.")

        protocol, status, keyword = parts

        if protocol != "HLN/0.1":
            raise Exception(f"Incorrect protocol, I only support HLN/0.1.")

        try:
            status = int(status)
        except ValueError:
            raise Exception(f"Status is not valid.")

        return status, keyword

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

    def add_server_key(self, server_key_b64):
        server_key = base64.b64decode(server_key_b64)
        result = self.gpg.import_keys(server_key)
        return result.fingerprints[0]

    def parse_decrypted_response(self, response):
        sections = response.split('\n\n')

        if len(sections) != 4:
            raise Exception(f"Incorrect number of sections, expected 4 but got {len(sections)}.")

        holoheader, server_key_b64, response_headers, body = sections

        status, keyword = self.parse_holoheader(holoheader)
        headers = self.parse_headers(response_headers)
        server_key_id = self.add_server_key(server_key_b64)

        return status, keyword, headers, body, server_key_id

    def get_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def get_server_key_id(self, hostname: str, port: int) -> str:
        server_key_id = self.server_key_ids.get(f"{hostname}:{port}")
        if not server_key_id:
            req = HoloLib.create_formatted_request("READ", "/server-key", self.gpg_key_b64)
            client_socket = self.get_socket()
            client_socket.connect((hostname, port))
            client_socket.sendall(req.encode('utf-8'))
            response = client_socket.recv(4096).decode('utf-8')
            response = HoloLib.decrypt_and_verify(response, gpg=self.gpg)
            print(response)
            client_socket.detach()
            status, keyword, headers, body, server_key_id = self.parse_decrypted_response(response)
            self.server_key_ids[f"{hostname}:{port}"] = server_key_id

        return server_key_id

    def send_request(self, method, resource, headers={}, body=''):
        request = HoloLib.create_formatted_request(
            method,
            resource,
            self.gpg_key_b64,
            headers,
            body
        )

        request = HoloLib.encrypt_and_sign(request, self.get_server_key_id(self.host, int(self.port)),
                                           self.gpg_key_id, gpg=self.gpg)

        client_socket = self.get_socket()
        client_socket.connect((self.host, self.port))
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(4096).decode('utf-8')
        response = HoloLib.decrypt_and_verify(response, gpg=self.gpg)
        print(f"Received response:\n{response}")
        client_socket.close()


if __name__ == '__main__':
    client = HoloNetClient()
    client.send_request('READ', '/')
    client.send_request('READ', '/hello-world')
    client.send_request('WRITE', '/update-user/12', {"Auth-Token": "TokenHere", "Content-Type": "application/json"}, json.dumps({"name":  "Sam"}))
