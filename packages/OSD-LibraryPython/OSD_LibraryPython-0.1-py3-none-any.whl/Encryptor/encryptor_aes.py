import logging
import os
import base64
from typing import Optional
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class AES:

    def __init__(self):
        # Tamaño de IV y Tag
        self.IV_LENGTH = 32  # AES-GCM usa un IV de 12 bytes
        self.TAG_LENGTH = 16  # AES-GCM usa un tag de autenticación de 16 bytes

    def encrypt_data(self, aes_key: str, data: str) -> Optional[str]:
        try:
            # Convertir la clave AES de base64 a bytes
            key = base64.b64decode(aes_key)

            # Generar un IV aleatorio (12 bytes para AES-GCM)
            iv = os.urandom(self.IV_LENGTH)

            # Crear el cifrador AES-GCM
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
            encryptor = cipher.encryptor()

            # Encriptar los datos
            ciphertext = encryptor.update(data.encode()) + encryptor.finalize()

            # Obtener el tag de autenticación
            tag = encryptor.tag

            # Devolver IV, datos cifrados y tag de autenticación en base64
            encrypted_data = iv + ciphertext + tag
            return base64.b64encode(encrypted_data).decode()
        except Exception as e:
            logging.error(f'Encryption error: {e}')
            return None

    def decrypt_data(self, aes_key: str, encrypted_data: str) -> Optional[str]:
        try:
            # Convertir la clave AES de base64 a bytes
            key = base64.b64decode(aes_key)

            # Decodificar los datos cifrados de base64
            encrypted_data = base64.b64decode(encrypted_data)

            # Extraer el IV (primeros 12 bytes)
            iv = encrypted_data[:self.IV_LENGTH]

            # Extraer el tag (últimos 16 bytes)
            tag = encrypted_data[-self.TAG_LENGTH:]

            # Extraer los datos cifrados (entre el IV y el tag)
            ciphertext = encrypted_data[self.IV_LENGTH:-self.TAG_LENGTH]

            # Crear el descifrador AES-GCM
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag))
            decryptor = cipher.decryptor()

            # Desencriptar los datos
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()

            return plaintext.decode()
        except Exception as e:
            logging.error(f'Decryption error: {e}')
            return None


