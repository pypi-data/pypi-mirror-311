import os
import asyncio
from json import dumps
from typing import Mapping
from datetime import datetime, timezone
from Helpers.services_bus import ServiceBus
from dotenv import load_dotenv
from azure.functions import HttpRequest

load_dotenv()

class CustomHttpRequest(HttpRequest):

    def __init__(self, method: str, url: str, headers: Mapping[str, str] = None, params: Mapping[str, str] = None, route_params:  Mapping[str, str] = None, body: bytes = None):
        # We call the constructor of the base class (HttpRequest)
        super().__init__(method, url, headers=headers, params=params, route_params=route_params, body=body)

        # Instantiate the Service Bus class to send messages
        self.service_bus = ServiceBus()

        asyncio.create_task(self.send_to_service_bus())

    async def send_to_service_bus(self) -> None:
        try:
            message_in = self.get_json()
            message_json = {
                'idMessageLog': self.headers.get('Idmessagelog'),
                'type': 'REQUEST',
                'environment': os.getenv('ENVIRONMENT'),
                'dateExecution': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                'header': dumps(dict(self.headers)),
                'microServiceUrl': self.url,
                'microServiceName': os.getenv('MICROSERVICENAME'),
                'microServiceVersion': os.getenv('MICROSERVICEVERSION'),
                'serviceName': message_in.get('operationName'),
                'machineNameUser': self.headers.get('Machinenameuser'),
                'ipUser': self.headers.get('Ipuser'),
                'userName': self.headers.get('Username'),
                'localitation': self.headers.get('Localitation'),
                'httpMethod': self.method,
                'httpResponseCode': '*',
                'messageIn': dumps(message_in),
                'messageOut': '*',
                'errorProducer': '*',
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