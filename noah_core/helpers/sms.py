from abc import ABCMeta, abstractmethod
import os
import requests


class SMSGateway(object):
    """
    Base class for all SMS gateway wrappers
    """
    __metaclass__ = ABCMeta


    @abstractmethod
    def send_sms(self, to_number, message, *args, **kwargs):
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


    def send_sms(self, to_number, message, *args, **kwargs):
        """
        The API endpoint used here is described in the `Kaleyra documentation <https://developers.kaleyra.com/docs/send-an-sms>`_

        :param to_number: Phone number to send the SMS to
        :type username: str
        :param message: Message to be sent
        :type message: str
        :return: Response from Kaleyra API endpoint
        """
        querystring = {
            'method': Kaleyra.METHOD,
            'api_key': Kaleyra.API_KEY,
            'sender': Kaleyra.SENDER_ID,
            'to': str(to_number),
            'message': message,
        }
        resp = requests.get(Kaleyra.API_ENDPOINT, params=querystring)
        return resp.json()
