import configparser
import pika
import logging

import json

from EmailNotifier import EmailNotifier
from SMSNotifier import SMSNotifier
from SMSNotifier_twilio import SMSNotifier_twilio

class NotificationInfo:
    actions = [
        'READY', 'RESERVED', 'CANCELLED'
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

            return NotificationInfo(user, email, phone, action, item)

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

logging.basicConfig(level=logging.DEBUG if config.get('logging', 'debug', fallback=False) else logging.INFO,
                    format="%(asctime)s [%(levelname)s] [%(name)s::%(lineno)d] %(message)s")

logger = logging.getLogger(__name__)

connection = None
channel = None

logger.info('Creating SES notifier')

email_notifier = EmailNotifier(
    key=config.get("aws", "aws_access_key_id"),
    secret=config.get("aws", "aws_secret_access_key"),
    region=config.get("aws", "aws_region")
)

logger.info('Creating SNS notifier')

sms_notifier = SMSNotifier(
    key=config.get("aws", "aws_access_key_id"),
    secret=config.get("aws", "aws_secret_access_key"),
    region=config.get("aws", "aws_region")
)

logger.info('Creating Twilio notifier')

sms_notifier_twilio = SMSNotifier_twilio(
    sid=config.get("twilio", "twilio_account_sid"),
    token=config.get("twilio", "twilio_auth_token"),
    sender=config.get("twilio", "twilio_sender")
)


try:
    logger.info('Connection to RMQ')

    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue, durable=True)

    logger.info('Successfully connected to RMQ')
except:
    logging.error('Could not connect to RMQ')
    exit(1)

def handle_message(channel, method_frame, header_frame, body):
    logger.info('Received message from queue')

    logger.debug(method_frame)
    logger.debug(header_frame)
    logger.info(body)

    try:
        info = NotificationInfo.from_string(body)

        logger.info('Attempting to send an email via SES')
        with email_notifier:
            email_notifier.send(info)
        
        #SEND SMS1
        logger.info('Attempting to send an SMS via SNS')
        with sms_notifier:
            sms_notifier.send(info)

        #SEND SMS2 (twilio)
        logger.info('Attempting to send an SMS via Twilio')
        with sms_notifier_twilio:
            sms_notifier_twilio.send(info)

        # Do stuff here
    except Exception as e:
        logger.error('Something went wrong')
        logger.exception(e)

    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

channel.basic_consume(queue, handle_message)

try:
    logger.info('Listening to message queue')
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
    logger.info('Exiting...')