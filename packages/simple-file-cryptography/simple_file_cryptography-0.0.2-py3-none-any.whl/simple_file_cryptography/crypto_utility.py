import os
from typing import Union
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def _encrypt_file(file_path_from: str, file_path_to: str, key: bytes):
    nonce = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
    encryptor = cipher.encryptor()

    with open(file_path_to, 'wb', buffering=33554432) as file_to:
        file_to.write(nonce)

        with open(file_path_from, 'rb', buffering=33554432) as file_from:
            while True:
                piece = file_from.read(16)
                file_to.write(encryptor.update(piece))

                if len(piece) < 16:
                    break

            file_to.write(encryptor.finalize())


def _decrypt_file(file_path_from: str, file_path_to: str, key: bytes):

    with open(file_path_from, 'rb', buffering=33554432) as file_from:
        nonce = file_from.read(16)
        cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
        decryptor = cipher.decryptor()
        with open(file_path_to, 'wb', buffering=33554432) as file_to:
            while True:
                piece = file_from.read(16)
                file_to.write(decryptor.update(piece))

                if len(piece) < 16:
                    break

            file_to.write(decryptor.finalize())


def encrypt_file(file_path_from: str, file_path_to: str, key: Union[bytes,
                                                                    str]):
    """
    Use this function to encrypt a file.
    
    Parameter `file_path_from` expects a string, representing
    the path to the file you wish to encrypt.
    
    Parameter `file_path_to` expects a string, representing the
    path to the file you wish to write to. This should end with `.enc`, but
    it does not have to.

    Parameter `key` expects a key, either in form of raw bytes or a
    hexadecimal string, that represents those bytes.
    """
    if type(key) is str:
        decoded_key = bytes.fromhex(key)
        _encrypt_file(file_path_from, file_path_to, decoded_key)
    if type(key) is bytes:
        _encrypt_file(file_path_from, file_path_to, key)


def decrypt_file(file_path_from: str, file_path_to: str, key: Union[bytes,
                                                                    str]):
    if type(key) is str:
        decoded_key = bytes.fromhex(key)
        _decrypt_file(file_path_from, file_path_to, decoded_key)
    if type(key) is bytes:
        _decrypt_file(file_path_from, file_path_to, key)


def generate_key(size: int = 16) -> bytes:
    """
    A simple convenience function that will generate 16 random bytes (128 bits).
    You may use `.hex()` method on received `bytes`, to get hexadecimal string
    representation.
    """
    return os.urandom(size)
