import logging

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

def _format_txt(info):
    if info.action == 'READY':
        txt = f'Your {info.item} is ready for pickup.'
    elif info.action == 'CANCELLED':
        txt = f'You have cancelled your reservation for {info.item}.'
    elif info.action == 'RESERVED':
        txt = f'You have made a reservation for {info.item}.'
    else:
        logger.warning(f"Invalid notification action {info.action}")
        raise ValueError(f"Invalid notification action {info.action}")

    return txt

class SMSNotifier:
    def __init__(self, key, secret, region):
        self.__key = key
        self.__secret = secret
        self.__region = region

        self.__client = None

    def __enter__(self):
        self.__client = boto3.client('sns',
                                     region_name=self.__region,
                                     aws_access_key_id=self.__key,
                                     aws_secret_access_key=self.__secret
                                     )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__client = None

    def send(self, info):
        phone_number = info.phone
        message = _format_txt(info)
        try:
            response = self.__client.publish(
                PhoneNumber=phone_number, Message=message)
            message_id = response['MessageId']
            logger.info("Published message id: %s.", phone_number)
        except ClientError:
            logger.exception("Couldn't publish message to %s.", phone_number)
            raise
        else:
            return message_id


