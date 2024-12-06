import os
import logging
from json import dumps
from typing import Optional
from dotenv import load_dotenv
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from azure.core.exceptions import AzureError

load_dotenv()
logging.basicConfig(level=logging.INFO)
class ServiceBus:
    def __init__(self):
        self.connection_str = os.getenv('CONNECTION_STRING')
        self.queue_name = os.getenv('QUEUE')

    async def send_message(self, message_json: dict) -> Optional[bool]:
        """Method to send a message to the Service Bus."""
        try:
            # Crear el cliente asincrónico para el Service Bus
            async with ServiceBusClient.from_connection_string(self.connection_str) as servicebus_client:
                # Crear el sender asincrónico para la cola
                async with servicebus_client.get_queue_sender(queue_name=self.queue_name) as sender:
                    # Crear el mensaje
                    message = ServiceBusMessage(dumps(message_json))

                    # Enviar el mensaje
                    await sender.send_messages(message)

            return True  # Indicar éxito

        except AzureError as e:
            logging.error(f'Error sending message to Service Bus: {e}')
            return None

        except Exception as e:
            logging.error(f'Unexpected error in Service Bus: {e}')
            return None
