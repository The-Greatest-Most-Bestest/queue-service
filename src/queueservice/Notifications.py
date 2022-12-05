import logging

import pika
import json

class NotificationPublisher:

    def __init__(self, host, username, password):
        self.__host = host
        self.__username = username
        self.__password = password

        self.__queue = 'qs-notifications'

        self.__creds = pika.PlainCredentials(username, password)
        self.__params = pika.ConnectionParameters(host=host, port=5672, credentials=self.__creds)

        self.__connection = None
        self.__channel = None

    def check(self):
        try:
            connection = self.__connect()
            connection.close()
        except Exception:
            logging.error("Could not connect to RMQ")
            raise


    def __connect(self):
        connection = pika.BlockingConnection(self.__params)
        self.__channel = connection.channel()
        self.__channel.queue_declare(self.__queue, durable=True)

        return connection

    def __enter__(self):
        self.__connection = self.__connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__connection:
            self.__connection.close()

    def publish(self, message:dict, action='READY'):
        message['action'] = action

        self.__channel.basic_publish(exchange='', routing_key=self.__queue, body=json.dumps(message))