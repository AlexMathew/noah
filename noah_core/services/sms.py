"""
At present, the app uses `Kaleyra <https://developers.kaleyra.com/>`_ for SMS integration. 

To use a new provider - 
1. Create the wrapper class in ``helpers/sms.py``, extending the ``SMSGateway`` class
2. Implement the ``send_sms`` method
3. Create a new ``SMSService`` object as
.. codeblock:: python

   xyz = SMSService(provider=sms.Xyz())

"""

import os
from ..helpers import sms


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


    def send(self, *, to_number=None, message=None, **kwargs):
        """
        Sends the message to the specified phone number. This is active only when the DEBUG env variable is false.
        The method takes the to_number and message (which should be keyword arguments), and other keyword arguments according to the provider.

        :param to_number: Phone number to send the SMS to
        :type username: str
        :param message: Message to be sent
        :type message: str
        """
        if not (os.getenv('DEBUG', 'true') == 'true'):
            resp = self.provider.send_sms(to_number, message, **kwargs)
            return resp
        else:
            print('SMS SENDING NOT AVAILABLE IN DEBUG MODE')


kaleyra = SMSService(provider=sms.Kaleyra())
