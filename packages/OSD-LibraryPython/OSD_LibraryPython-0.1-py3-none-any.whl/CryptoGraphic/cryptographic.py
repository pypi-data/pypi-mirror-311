from base64 import b64decode, b64encode
import os
import jwt
import pytz
import logging
import uuid
from typing import Tuple, Dict, Optional, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from Helpers.database import DBConnection
# Configuración del log
logging.basicConfig(level=logging.INFO)

load_dotenv()

class TokenManager:

    def __init__(self):
        self.db = DBConnection()
        self.conn = self.db.get_db_connection()
        self.cursor = self.conn.cursor()
        self.jwt_secret_key = os.getenv('JWT_SECRET_KEY')
        self.public_key2, self.private_key1, self.private_key2 = self.__get_rsa_keys()

    def decrypt_string(self, encrypted_string:str, public_version:str='public1') -> Optional[str]:
        try:
            encrypted_str = TokenManager.__decode_base64(encrypted_string)
            if public_version == 'public1':
                private_key = serialization.load_pem_private_key(self.private_key1.encode('utf-8'), password=None)
            else:
                private_key = serialization.load_pem_private_key(self.private_key2.encode('utf-8'), password=None)

            text = private_key.decrypt(
                encrypted_str,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            return text.decode()

        except Exception as e:
            logging.error(f'Error decrypting string: {e}')
            return None

    def generate_token(self, time_zone:str, name_legacy: Optional[str] = None, token: Optional[str] = None, user_id: Optional[str] = None):
        if name_legacy and (token or user_id):
            raise ValueError("'name_legacy' cannot be used together with 'token' or 'user_id'.")

        payload_data = None
        access_token = None
        access_token_expiration = None

        if name_legacy:
            legacy_id, enterprise_id, token_expiration_minutes = self.__get_data_legacy(name_legacy=name_legacy)
            payload_data = {
                'authorization_id': str(uuid.uuid4()),
                'legacy_id': legacy_id,
                'enterprise_id': enterprise_id,
                'token_expiration': token_expiration_minutes,
                'key_aes': TokenManager.__generate_key_aes()
            }

        if token and user_id:
            payload = self.extract_payload_jwt(token)
            _, _, token_expiration_minutes = self.__get_data_legacy(legacy_id=payload.get('legacy_id'))
            access_token, access_token_expiration = self.__get_data_authorization(authorization_id=payload.get('authorization_id'))
            payload_data = {
                'authorization_id': payload.get('authorization_id'),
                'user_id': user_id,
                'token_expiration': token_expiration_minutes
            }

        payload = TokenManager.__build_payload(time_zone=time_zone, payload_data=payload_data)
        generated_token = self.__generate_jwt_token(payload)

        if not token:
            generated_token  = self.__encrypt_token(generated_token)

        return_payload_data = payload_data.copy()
        if access_token and access_token_expiration:
            return_payload_data.update({
                'access_token': access_token,
                'access_token_expiration': access_token_expiration
            })

        return return_payload_data, generated_token

    # Metodos helpers
    @staticmethod
    def __decode_base64(encoded_string: str) -> bytes:
        return b64decode(encoded_string)

    def __get_rsa_keys(self) -> Optional[Tuple[str, str, str]]:
        try:
            self.cursor.execute('EXEC SECURITY.sps_SelectKeys')
            row = self.cursor.fetchone()
            status_code = row[0]
            if status_code != 'DB_0004':
                raise ValueError('Error retrieving RSA keys from the database.')

            public_key2 = row[2]
            private_key1 = row[3]
            private_key2 = row[4]

            return public_key2, private_key1, private_key2

        except Exception as e:
            logging.error(f'Error fetching keys: {e}')
            return None

    def __get_data_legacy(self, name_legacy: str = None, legacy_id: str = None) -> Optional[Tuple[str, str, int]]:
        try:
            self.cursor.execute('EXEC SECURITY.sps_SelectDataLegacy @i_nameLegacy = ?, @i_idLegacy = ?',
                                (name_legacy, legacy_id))
            row = self.cursor.fetchone()
            status_code = row[0]
            if status_code != 'DB_0004':
                raise ValueError('Error retrieving data from the legacy table in the database.')

            id_legacy = row[2]
            id_enterprise = row[3]
            token_expiration_minutes  = row[4]

            return id_legacy, id_enterprise, token_expiration_minutes

        except Exception as e:
            logging.error(f'Error fetching legacy data: {e}')
            return None

    def __get_data_authorization(self, authorization_id: str) -> Optional[Tuple[str, datetime]]:
        try:
            self.cursor.execute('EXEC SECURITY.sps_SelectAuthorization @i_idAuthorization = ?',(authorization_id,))
            row = self.cursor.fetchone()
            status_code = row[0]
            if status_code != 'DB_0004':
                raise ValueError('Error retrieving data from the legacy table in the database.')

            access_token = row[2]
            access_token_expiration = row[3]

            return access_token, access_token_expiration

        except Exception as e:
            logging.error(f'Error fetching legacy data: {e}')
            return None

    def extract_payload_jwt(self, decoded_jwt: str) -> Optional[dict]:
        try:
            payload = jwt.decode(decoded_jwt, self.jwt_secret_key, algorithms=['HS256'])
            return payload

        except jwt.ExpiredSignatureError as jwt_expired:
            logging.error(f'Error Token Expired: {jwt_expired}')
            return None

        except jwt.InvalidTokenError as jwt_invalid:
            logging.error(f'Error Token Invalid: {jwt_invalid}')
            return None

        except Exception as e:
            logging.error(f'Unexpected Error: {e}')
            return None

    @staticmethod
    def __build_payload(time_zone:str, payload_data: dict) -> Dict[str, any]:
        token_expired_str = TokenManager.__get_token_expiry_time(time_zone, payload_data.get('token_expiration'))
        payload_data['token_expiration'] = token_expired_str
        return payload_data

    @staticmethod
    def __get_token_expiry_time(time_zone: str, time: int) -> str:
        timezone = pytz.timezone(time_zone)
        current_time = datetime.now(timezone)
        token_expired = current_time + timedelta(minutes=time)
        token_expired_str = token_expired.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        return token_expired_str

    def __generate_jwt_token(self, payload: dict) -> Optional[str]:
        try:
            if not self.jwt_secret_key:
                raise ValueError('JWT secret key not found in .env file')

            token = jwt.encode(payload, self.jwt_secret_key, algorithm='HS256')
            return token

        except Exception as e:
            logging.error(f'Error generating JWT token: {e}')
            return None

    def __encrypt_token(self, jwt_token: str) -> Optional[str]:
        try:
            public_key = serialization.load_pem_public_key(self.public_key2.encode('utf-8'))
            token_bytes = jwt_token.encode('utf-8')
            # Cifrar con la clave pública RSA
            encrypted_token = public_key.encrypt(
                token_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            access_token = b64encode(encrypted_token).decode('utf-8')
            return access_token

        except Exception as e:
            logging.error(f'Error encrypting token: {e}')
            return None

    @staticmethod
    def __generate_key_aes() -> str:
        key =  os.urandom(32)
        return b64encode(key).decode('utf-8')

