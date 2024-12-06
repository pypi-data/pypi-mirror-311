import os
import logging
from typing import Optional
from pyodbc import connect, Connection
from dotenv import load_dotenv

load_dotenv()

class DBConnection:

    def __init__(self):
        self.connection_string = os.getenv('DATABASE')

    def get_connection(self) -> Optional[Connection]:
        if not self.connection_string:
            raise ValueError('The environment variable DATABASE is not defined')

        connection = connect(self.connection_string)
        if connection is None:
            raise ValueError('Error connecting to database')

        return connection
