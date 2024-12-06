import jwt
from Exceptions.exceptions import JWTokenError

class JWT:

    @staticmethod
    def generate_token(payload: dict, jwt_secret_key:str) -> str:
        try:
            token = jwt.encode(payload, jwt_secret_key, algorithm='HS256')
            return token

        except Exception as ex:
            raise JWTokenError(error=str(ex)) from ex

    @staticmethod
    def extract_payload(jwt_token: str, jwt_secret_key:str) -> dict:
        try:
            payload = jwt.decode(jwt_token, jwt_secret_key, algorithms=['HS256'])
            return payload

        except Exception as ex:
            raise JWTokenError(error=str(ex)) from ex