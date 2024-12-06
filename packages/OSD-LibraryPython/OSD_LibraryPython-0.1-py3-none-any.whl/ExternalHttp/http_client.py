import os
from typing import Optional, Dict, Any
from requests import Session, Response
from json import dumps
from datetime import datetime
from dotenv import load_dotenv
from Helpers.services_bus import ServiceBus
from azure.functions import HttpRequest
from tzlocal import get_localzone

load_dotenv()

class HttpClientError(Exception):
    """Base exception for errors related to JWT Token."""
    pass

class HttpClient(Session):

    def __init__(self, base_url:str, request:HttpRequest, token:str=None):
        """
        Initializes an HTTP session with optional settings:

        :param base_url: (str) Base URL of the external API.
        :param request: (HttpRequest) HTTP request object (used to extract headers).
        :param token: (str, optional): Authorization token to include in request headers.
        """
        super().__init__()
        self.base_url = base_url
        self.request = request
        self.local_tz = get_localzone()
        self.service_bus = ServiceBus()

        if token:
            self.headers.update({
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            })

    def post(self, endpoint:str, data:Optional[Dict[str,Any]]=None, json:Dict[str,Any]=None, **kwargs) -> Response:
        """
        Constructs the full URL by concatenating base_url and endpoint.
        Send a record of the request to the Service Bus with the send_request_to_service_bus method.
        Make the POST request using the base class method (Session.post).
        Send a record of the response to the Service Bus with the send_response_to_service_bus method.
        Returns the Response object.

        :param endpoint: (str) API-specific path (concatenated with base_url).
        :param data: (Dict[str, Any], optional): Data to send in the request body (x-www-form-urlencoded format).
        :param json: (Dict[str, Any], optional): Data to send in JSON format.

        :return: Returns the Response object
        """
        try:
            url = self.base_url + endpoint
            self.send_request_to_service_bus(endpoint=url, body=json)
            response = super().post(url, data=data, json=json, **kwargs)
            self.send_response_to_service_bus(response)

            return response

        except Exception as e:
            raise HttpClientError(f'Error when making the request: {str(e)}')

    async def send_request_to_service_bus(self, endpoint:str, body:Dict[str,Any]) -> Optional[bool]:
        """
        Send a message to the Service Bus with details about the request made:

        :param endpoint: (str): URL of the endpoint to which the request will be made.
        :param body: (Dict[str, Any]): Body of the request (usually in JSON format).
        """
        try:
            headers = self.request.headers
            message_json = {
                'idMessageLog': headers.get('Idmessagelog'),
                'type': 'REQUEST',
                'environment': os.getenv('ENVIRONMENT'),
                'dateExecution': datetime.now(self.local_tz).strftime('%Y-%m-%d %H:%M:%S'),
                'header':  dumps(dict(headers)),
                'microServiceUrl': endpoint,
                'microServiceName': os.getenv('MICROSERVICENAME'),
                'microServiceVersion': os.getenv('MICROSERVICEVERSION'),
                'serviceName': body.get('operationName'),
                'machineNameUser': headers.get('Machinenameuser'),
                'ipUser': headers.get('Ipuser'),
                'userName': headers.get('Username'),
                'localitation': headers.get('Localitation'),
                'httpMethod': 'POST',
                'httpResponseCode': '*',
                'messageIn': dumps(body),
                'messageOut': '*',
                'errorProducer': '*',
                'auditLog': 'MESSAGE_LOG_EXTERNAL'
            }

            return await self.service_bus.send_message(message_json)

        except Exception as e:
            self.handle_enqueue_failure(e)

    async def send_response_to_service_bus(self, response: Response) -> Optional[bool]:
        """
        Send a message to the Service Bus with details about the response received:

        :param response: (Response): Response object received from the endpoint.
        """
        try:
            headers = self.request.headers
            message_json = {
                'idMessageLog': headers.get('Idmessagelog'),
                'type': 'RESPONSE',
                'dateExecution': datetime.now(self.local_tz).strftime('%Y-%m-%d %H:%M:%S'),
                'httpResponseCode': str(response.status_code),
                'messageOut': dumps(response.json()),
                'auditLog': 'MESSAGE_LOG_EXTERNAL'
            }

            return await self.service_bus.send_message(message_json)

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