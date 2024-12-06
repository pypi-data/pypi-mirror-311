import hashlib
import os

class Encryptor:

    @staticmethod
    def __generate_salt():
        """Genera un salt aleatorio de 16 bytes."""
        return os.urandom(16)

    @staticmethod
    def hash_password(password: str, salt: bytes = None) -> str:
        """Genera el hash SHA-512 de una contraseña con un salt."""
        if salt is None:
            salt = Encryptor.__generate_salt()  # Si no se pasa un salt, se genera uno.

        # Concatenamos el salt con la contraseña.
        salted_password = password.encode('utf-8') + salt

        # Calculamos el hash SHA-512
        hash_object = hashlib.sha512(salted_password)
        hashed_password = hash_object.hexdigest()

        # Devolvemos el hash junto con el salt utilizado (para verificar más tarde).
        return f"{salt.hex()}${hashed_password}"

    @staticmethod
    def verify_password(stored_password: str, password: str) -> bool:
        """Verifica si la contraseña proporcionada coincide con el hash almacenado."""
        salt_hex, stored_hash = stored_password.split('$')
        salt = bytes.fromhex(salt_hex)

        # Generamos el hash de la contraseña proporcionada con el mismo salt.
        return Encryptor.hash_password(password, salt).split('$')[1] == stored_hash

