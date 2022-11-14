import configparser
import pika
import logging

import json

from EmailNotifier import EmailNotifier
from SMSNotifier import SMSNotifier

class NotificationInfo:
    actions = [
        'READY', 'QUEUED', 'CANCELLED'
    ]

    def __init__(self, user, email, phone, action, item=None):
        self.user = user
        self.email = email
        self.phone = phone
        self.action = action
        self.item = item if item is not None else 'item'

    @staticmethod
    def from_string(json_string):
        try:
            parsed = json.loads(json_string)

            user = parsed['name']
            contact_info = parsed['contact_info']
            email = contact_info['email']
            phone = contact_info['phone']

            item = None

            try:
                item = parsed['item']
            except KeyError:
                pass

            action = parsed['action']

            if action not in NotificationInfo.actions:
                logging.warning(f'Action ({action}) is not valid. Ignoring')
                raise KeyError()

            return NotificationInfo(user, email, phone, item)

        except KeyError as e:
            logging.exception("Missing required info in JSON object from RMQ")
            logging.exception(e)
            raise
        except Exception as e:
            logging.exception(e)
            raise

config = configparser.ConfigParser()
config.read_file(open('config/config.ini', 'r'))

host = config.get('rmq', 'host')
username = config.get("rmq", "username")
password = config.get("rmq", "password")

queue = config.get("rmq", 'queue', fallback='qs-notifications')

creds = pika.PlainCredentials(username, password)
params = pika.ConnectionParameters(host=host, port=5672, credentials=creds)

connection = None
channel = None

email_notifier = EmailNotifier(
    key=config.get("aws", "aws_access_key_id"),
    secret=config.get("aws", "aws_secret_access_key"),
    region=config.get("aws", "aws_region")
)

try:
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue, durable=True)
except:
    logging.error('Could not connect to RMQ')
    exit(1)

def handle_message(channel, method_frame, header_frame, body):
    print(method_frame)
    print(header_frame)
    print(body)
    print()

    try:
        info = NotificationInfo.from_string(body)

        with email_notifier:
            email_notifier.send(info)

        # Do stuff here
    except:
        pass

    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

channel.basic_consume(queue, handle_message)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()