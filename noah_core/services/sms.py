"""
At present, the app uses `Kaleyra <https://developers.kaleyra.com/>`_ for SMS integration. 

To use a new provider - 
1. Create the wrapper class, extending the ``SMSGateway`` class
2. Implement the ``send_sms`` method
3. Create a new ``SMSService`` object as
.. codeblock:: python

   xyz = SMSService(provider=Xyz())

"""

from abc import ABCMeta, abstractmethod
import os
import requests
from noah.celery import app

class SMSGateway(object):
    """
    Base class for all SMS gateway wrappers
    """
    __metaclass__ = ABCMeta


    @abstractmethod
    def send_sms(self, to_number, message_content, *args, **kwargs):
        pass


class Kaleyra(SMSGateway):
    """
    Wrapper around `Kaleyra <https://developers.kaleyra.com/>`_ for SMS integration

    ``KALEYRA_API_KEY`` and ``KALEYRA_SENDER_ID`` should be set as env variables
    """
    API_KEY = os.getenv("KALEYRA_API_KEY") or None
    SENDER_ID = os.getenv("KALEYRA_SENDER_ID") or None
    METHOD = 'sms'
    API_ENDPOINT = 'https://api-alerts.kaleyra.com/v4/'


    def __init__(self):
        """
        """
        pass


    def send_sms(self, to_number, message_content, *args, **kwargs):
        """
        The API endpoint used here is described in the `Kaleyra documentation <https://developers.kaleyra.com/docs/send-an-sms>`_

        :param to_number: Phone number to send the SMS to
        :type username: str
        :param message_content: Message to be sent
        :type message_conten: str
        :return: Response from Kaleyra API endpoint
        """
        querystring = {
            'method': Kaleyra.METHOD,
            'api_key': Kaleyra.API_KEY,
            'sender': Kaleyra.SENDER_ID,
            'to': str(to_number),
            'message': message_content,
        }
        resp = requests.get(Kaleyra.API_ENDPOINT, params=querystring)
        return resp.json()


class SMSService:
    """
    Service for sending text messages. Wraps the helper for any SMS gateway, as defined in helpers/sms.py
    """
    def __init__(self, provider):
        """
        Initializes the SMS service using a particular provider

        :param: SMS gateway to be used
        :type: object of helper class
        """
        self.provider = provider


    def send(self, *, to_number=None, message_content=None, **kwargs):
        """
        Sends the message to the specified phone number. This is active only when the DEBUG env variable is false.
        The method takes the to_number and message (which should be keyword arguments), and other keyword arguments according to the provider.

        :param to_number: Phone number to send the SMS to
        :type username: str
        :param message_content: Message to be sent
        :type message_content: str
        """
        if not (os.getenv('DEBUG', 'true') == 'true'):
            if not (to_number and message_content):
                raise Exception('`to_number` and `message_content` cannot be None')
            resp = self.provider.send_sms(to_number, message_content, **kwargs)
            return resp
        else:
            print('SMS SENDING NOT AVAILABLE IN DEBUG MODE')


kaleyra = SMSService(provider=Kaleyra())


@app.task(name='services.sms.send_sms')
def send_sms(to_number=None, message_content=None):
    """
    Sample placeholder celery task for sending SMS.

    ``send_sms.delay(to_number='', message_content='')``
    """
    resp = kaleyra.send(to_number=to_number, message_content=message_content)
