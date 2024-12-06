import json
from base64 import b64decode, b64encode
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from Exceptions.exceptions import RSAEncryptError

class RSAEncryptor:

    @staticmethod
    def encrypt(data: str | dict, public_key_rsa: str) -> str:
        try:
            if isinstance(data, dict):
                data = json.dumps(data)

            public_key = serialization.load_pem_public_key(public_key_rsa.encode('utf-8'))
            data_bytes = data.encode('utf-8')
            encrypted_bytes = public_key.encrypt(
                data_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            return b64encode(encrypted_bytes).decode('utf-8')

        except Exception as ex:
            raise RSAEncryptError(error=str(ex)) from ex

    @staticmethod
    def decrypt(data: str, private_key_rsa: str) -> str:
        try:
            encrypted_bytes = b64decode(data)
            private_key = serialization.load_pem_private_key(private_key_rsa.encode('utf-8'), password=None)
            decrypted_bytes = private_key.decrypt(
                encrypted_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            return decrypted_bytes.decode('utf-8')

        except Exception as ex:
            raise RSAEncryptError(error=str(ex)) from ex



