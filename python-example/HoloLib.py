import gnupg


def create_formatted_request(method: str, resource: str, client_public_key: str, headers=None, body="",
                             protocol="HLN/0.1"):
    """

    :param method: The method of the request
    :param resource: The requested resource on the server
    :param client_public_key: The public key encaoded as a single line b64 str
    :param headers:
    :param body:
    :param protocol:
    :return:
    """
    if headers is None:
        headers = {}

    if method is None or resource is None or client_public_key is None:
        raise ValueError("Method, resource and public key must be specified")

    headers_formatted = ""

    if len(headers) < 1:
        headers_formatted = "\n\n"
    else:
        for key, value in headers.items():
            headers_formatted += f"{key}: {value}\n"
        headers_formatted += "\n"

    return f"{protocol} {method} {resource}\n\n{client_public_key}\n\n{headers_formatted}{body}"


def create_formatted_response(status: int, message: str, server_public_key: str, headers=None, body="",
                              protocol="HLN/0.1"):
    if headers is None:
        headers = {}

    if status is None or message is None or server_public_key is None:
        raise ValueError("Status, message and public key must be specified")

    headers_formatted = ""

    if len(headers) < 1:
        headers_formatted = "\n\n"
    else:
        for key, value in headers.items():
            headers_formatted += f"{key}: {value}\n"
        headers_formatted += "\n"

    return f"{protocol} {status} {message}\n\n{server_public_key}\n\n{headers_formatted}{body}"


def encrypt_and_sign(data, recipient_key_id, sender_key_id, passphrase=None, gpg=None):
    """
    Encrypts and signs a string using GnuPG.

    :param gpg: gnupg.GPG object
    :param data: string to encrypt and sign
    :param recipient_key_id: GPG key ID of the recipient
    :param sender_key_id: GPG key ID of the sender
    :param passphrase: passphrase for the sender's private key
    :return: encrypted and signed data
    """
    gpg = gpg or gnupg.GPG()

    if passphrase:
        encrypted_data = gpg.encrypt(data, recipients=[recipient_key_id], sign=sender_key_id, passphrase=passphrase)
    else:
        encrypted_data = gpg.encrypt(data, recipients=[recipient_key_id], sign=sender_key_id)
    if not encrypted_data.ok:
        raise ValueError(f"Encryption failed: {encrypted_data.stderr}")
    return str(encrypted_data)


def decrypt_and_verify(encrypted_data, passphrase=None, gpg=None):
    """
    Decrypts and verifies a string using GnuPG.

    :param gpg: gnupg.GPG object
    :param encrypted_data: encrypted string to decrypt and verify
    :param passphrase: passphrase for the recipient's private key
    :return: decrypted data and verification status
    """
    gpg = gpg or gnupg.GPG()

    decrypted_data = gpg.decrypt(encrypted_data, passphrase=passphrase) if passphrase else gpg.decrypt(encrypted_data)
    if not decrypted_data.ok:
        raise ValueError(f"Decryption failed: {decrypted_data.stderr}")
    return decrypted_data.data.decode('utf-8')
