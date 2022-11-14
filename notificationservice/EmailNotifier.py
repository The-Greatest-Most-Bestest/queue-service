import logging

import boto3
from botocore.exceptions import ClientError

class EmailNotifier:
    def __init__(self, key, secret, region):
        self.__key = key
        self.__secret = secret
        self.__region = region

        self.__client = None

    def __enter__(self):
        self.__client = boto3.client('ses', region_name=self.__region)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__client = None

    def send(self, info):
        sender = "Do Not Reply <no-reply@notifications.cpp-queue.com>"
        recipient = info.email

        subject = 'Your item is ready for pickup'

        body_text = 'TBD'

        body_html = """
        <html>
        <head></head>
        <body>
        <h1>TBD</h1>
        </body>
        </html>
        """

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
            logging.exception(e)
        else:
            logging.info(f'Email sent! Message ID: {response["MessageId"]}')
