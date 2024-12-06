import asyncio
from typing import Dict, Any
from json import dumps
from datetime import datetime, timezone
from azure.functions import HttpResponse, HttpRequest
from Helpers.services_bus import ServiceBus

class CustomHttpResponse(HttpResponse):

    def __init__(self, data:dict|None, status_code:int=200, message:str=None, headers:Dict[str,Any]=None, mimetype:str='application/json', charset:str='utf-8', request:HttpRequest=None):
        """
        HttpResponse constructor overload.
        """
        self.service_bus = ServiceBus()
        self.request = request
        self.data = dumps(data)
        headers = headers or {}
        headers.setdefault('Content-Type', mimetype)

        response = {
            'status' : status_code,
            'message' : message,
            'data' : data
        }

        # Call the constructor of the HttpResponse base class with the appropriate parameters
        super().__init__(body=dumps(response), status_code=status_code, headers=headers, mimetype=mimetype, charset=charset)
        if status_code == 200:
            asyncio.create_task(self.send_to_service_bus())

    async def send_to_service_bus(self) -> None:
        try:
            headers = self.request.headers
            id_message_log = headers.get('Idmessagelog')
            message_json = {
                'idMessageLog': id_message_log,
                'type': 'RESPONSE',
                'dateExecution': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                'httpResponseCode': str(self.status_code),
                'messageOut': self.data,
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