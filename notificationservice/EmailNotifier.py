import logging

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


def _format_html(info):
    if info.action == 'READY':
        html = open('templates/email_ready.template.html').read().format(info.user, info.item)
    elif info.action == 'CANCELLED':
        html = open('templates/email_cancelled.template.html').read().format(info.name, info.item)
    elif info.action == 'RESERVED':
        html = open('templates/email_reserved.template.html').read().format(info.name, info.item)
    else:
        logger.warning(f"Invalid notification action {info.action}")
        raise ValueError(f"Invalid notification action {info.action}")

    return html


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

class EmailNotifier:
    def __init__(self, key, secret, region):
        self.__key = key
        self.__secret = secret
        self.__region = region

        self.__client = None

    def __enter__(self):
        self.__client = boto3.client('ses',
                                     region_name=self.__region,
                                     aws_access_key_id=self.__key,
                                     aws_secret_access_key=self.__secret
                                     )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__client = None

    def send(self, info):
        sender = "Do Not Reply <no-reply@notifications.cpp-queue.com>"
        recipient = info.email

        subject = 'Your item is ready for pickup'

        body_text = _format_txt(info)
        body_html = _format_html(info)

        charset = 'UTF-8'

        try:
            response = self.__client.send_email(
                Destination={
                    'ToAddresses': [
                        recipient
                    ]
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': charset,
                            'Data': body_html
                        },
                        'Text': {
                            'Charset': charset,
                            'Data': body_text
                        }
                    },
                    'Subject': {
                        'Charset': charset,
                        'Data': subject
                    }
                },
                Source=sender
            )
        except ClientError as e:
            logger.error(e.response['Error']['Message'])
        else:
            logger.info(f'Email sent! Message ID: {response["MessageId"]}')
