
import os
from base64 import b64decode, b64encode
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from typing import Dict
from Exceptions.exceptions import AESEncryptError


class AES:
    def __init__(self):
        self.IV_LENGTH = 32
        self.TAG_LENGTH = 16

    @staticmethod
    def generate_key() -> str:
        """Generates a random 256-bit AES key and returns it Base64 encoded."""
        key = os.urandom(32)
        return b64encode(key).decode('utf-8')

    def encrypt(self, aes_key: str, data: Dict) -> str:
        """
        Encrypts data using AES-GCM.
        Only supports dictionary objects.

        :param aes_key: AES key in Base64 format.
        :param data: Data to be encrypted (dict).
        :return: Data encrypted in Base64.
        """
        if not isinstance(data, dict):
            raise ValueError('Input data must be a dictionary.')

        try:
            # Convert AES key from Base64 to bytes
            key = b64decode(aes_key)

            # Generate a random IV (32 bytes for AES-GCM)
            iv = os.urandom(self.IV_LENGTH)

            # Convert the dictionary to JSON string
            json_data = json.dumps(data)

            # Create the AES-GCM encryptor
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
            encryptor = cipher.encryptor()

            # Encrypt data
            ciphertext = encryptor.update(json_data.encode('utf-8')) + encryptor.finalize()

            # Get the authentication tag
            tag = encryptor.tag

            # Return IV, encrypted data and authentication tag in Base64
            encrypted_data = iv + ciphertext + tag

            return b64encode(encrypted_data).decode('utf-8')

        except Exception as ex:
            raise AESEncryptError(error=str(ex)) from ex

    def decrypt(self, aes_key: str, encrypted_data: str) -> Dict:
        """
        Decrypts data using AES-GCM.
        Expects encrypted data to represent a JSON object.

        :param aes_key: AES key in Base64 format.
        :param encrypted_data: Data encrypted in Base64.
        :return: Decrypted data (dict).
        """
        try:
            # Convert AES key from Base64 to bytes
            key = b64decode(aes_key)

            # Decode Base64 encrypted data
            encrypted_data = b64decode(encrypted_data)

            # Extract the IV (first 32 bytes)
            iv = encrypted_data[:self.IV_LENGTH]

            # Extract the tag (last 16 bytes)
            tag = encrypted_data[-self.TAG_LENGTH:]

            # Extract the encrypted data (between the IV and the tag)
            ciphertext = encrypted_data[self.IV_LENGTH:-self.TAG_LENGTH]

            # Create the AES-GCM decryptor
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag))
            decryptor = cipher.decryptor()

            # Decrypt the data
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()

            # Convert the decrypted plaintext to a dictionary
            return json.loads(plaintext.decode('utf-8'))

        except json.JSONDecodeError as ex:
            raise AESEncryptError(error=str(ex)) from ex

        except Exception as ex:
            raise AESEncryptError(error=str(ex)) from ex
