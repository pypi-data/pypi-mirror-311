import os
from Encryptor.rsa_encrypt import RSAEncryptor
from Encryptor.jwt import JWT
from Helpers.database import DBConnection
from Exceptions.exceptions import DatabaseError
from pyodbc import Error

class ValidationTokenError(Exception):
    pass

class ValidationToken:

    def __init__(self, private_key):
        self.private_key = private_key
        self.JWT_ACCESS_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
        self.db = DBConnection()
        self.conn = self.db.get_connection()
        self.cursor = self.conn.cursor()

    def __validate_access_token(self, authorization_id:str, access_token:str) -> bool:
        try:
            self.cursor.execute("""
            EXEC SECURITY.sps_ValidateToken
            @i_idAuthorization = ?,
            @i_accessToken = ?
            """, (authorization_id, access_token))
            result = self.cursor.fetchone()

            if result.STATUS_CODE != 'DB_0004':
                return False

            self.conn.commit()
            return True

        except Error as e:
            self.conn.rollback()
            raise DatabaseError(f'Error validating token in database: {str(e)}')

    def validate(self, encrypt_token:str) -> dict:
        try:
            access_token = RSAEncryptor.decrypt(encrypt_token, self.private_key)
            payload = JWT.extract_payload(access_token, self.JWT_ACCESS_SECRET_KEY)
            if self.__validate_access_token(payload.get('authorization_id'), encrypt_token):
                return {
                    'legacy_id': payload.get('legacy_id'),
                    'authorization_id': payload.get('authorization_id'),
                    'enterprise_id': payload.get('enterprise_id'),
                    'key_aes': payload.get('key_aes'),
                    'user_id': '00000000-0000-0000-0000-000000000000',
                    'profile_id': '00000000-0000-0000-0000-000000000000',
                    'token_id': '00000000-0000-0000-0000-000000000000',
                    'status': 200
                }

            return {
                'legacy_id': '00000000-0000-0000-0000-000000000000',
                'authorization_id': '00000000-0000-0000-0000-000000000000',
                'enterprise_id': '00000000-0000-0000-0000-000000000000',
                'user_id': '00000000-0000-0000-0000-000000000000',
                'profile_id': '00000000-0000-0000-0000-000000000000',
                'token_id': '00000000-0000-0000-0000-000000000000',
                'status': 401
            }
        except Exception as e:
            raise ValidationTokenError(f'Error validating token {str(e)}')

