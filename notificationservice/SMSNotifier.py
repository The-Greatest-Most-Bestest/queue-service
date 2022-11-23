import logging

import boto3
from botocore.exceptions import ClientError

class SMSNotifier:
    def __init__(self, key, secret, region):
        self.__key = key
        self.__secret = secret
        self.__region = region

        self.__client = None

    def __enter__(self):
        self.__client = boto3.client('ses', region_name=self.__region)

    def send(self, info):
        phone_number = info.phone
        message = 'Your queue is ready'
        try:
            response = self.sns_resource.meta.client.publish(
                PhoneNumber=phone_number, Message=message)
            message_id = response['MessageId']
            logger.info("Published message to %s.", phone_number)
        except ClientError:
            logger.exception("Couldn't publish message to %s.", phone_number)
            raise
        else:
            return message_id


