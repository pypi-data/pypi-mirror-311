import logging
import asyncio
from typing import Any
from datetime import datetime
from tzlocal import get_localzone
from Helpers.services_bus import ServiceBus
from azure.functions import HttpRequest

class OSDException(Exception):
    """ Base class for all custom exceptions. """

    def __init__(self, message:str='The operation was not completed.', error:Any=None, status_code:int=400, request:HttpRequest=None):
        super().__init__(message)
        self.message = message
        self.error = error
        self.request = request
        self.status_code = status_code
        self.local_tz = get_localzone()
        self.service_bus = ServiceBus()
        asyncio.create_task(self.send_to_service_bus())

    async def send_to_service_bus(self) -> None:
        """ Method to send a message to the Service Bus. """
        try:
            if not self.request:
                raise ValueError('There is no data in the request')

            id_message_log = self.request.headers.get('Idmessagelog')
            message_json = {
                'idMessageLog': id_message_log,
                'type': 'ERROR',
                'dateExecution': datetime.now(self.local_tz).strftime('%Y-%m-%d %H:%M:%S'),
                'httpResponseCode': str(self.status_code),
                'messageOut': '*',
                'errorProducer': self.error,
                'auditLog': 'MESSAGE_LOG_INTERNAL'
            }

            await self.service_bus.send_message(message_json)

        except Exception as e:
            self.handle_enqueue_failure(e)

    @staticmethod
    def handle_enqueue_failure(exception: Exception) -> None:
        """ Handles failures in sending to the Service Bus. """
        # Here you can perform actions like:
        # 1. Log the error locally.
        # 2. Send the error to another alternative system.
        # 3. Store the message in a file or database for later retry.
        print(f'Error enqueuing message in Service Bus: {str(exception)}')


class OSDHttpError(OSDException):
    pass

class OSDNotAuthorized(OSDException):
    pass

class DatabaseError(OSDException):
    pass

class RSAEncryptError(OSDException):
    pass

class AESEncryptError(OSDException):
    pass

class JWTokenError(OSDException):
    pass