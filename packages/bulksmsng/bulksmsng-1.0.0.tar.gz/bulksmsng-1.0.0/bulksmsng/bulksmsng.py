import requests

SEND_SMS_URL = 'https://www.bulksmsnigeria.com/api/v2/sms'
GET_SMS_BALANCE_URL = "https://www.bulksmsnigeria.com/api/v2/balance"
GET_DELIVERY_REPORT_URL = "https://www.bulksmsnigeria.com/api/v2/delivery"


class BulkSMSNigeria:
    def __init__(self, api_token) -> None:
        """
        Initializes an instance of the BulkSMSNigeria class.

        Args:
            api_token (str): The API token for authenticating requests.
        """

        self.api_token = api_token

    def sendToOne(self, sender, recipient, body, gateway="direct-refund", append_sender='hosted'):
        """
        Sends an SMS to a single recipient.

        Args:
            sender (str): The sender's name or number.
            recipient (str): The recipient's phone number.
            body (str): The message content.
            gateway (str, optional): The gateway to use for sending the SMS. Defaults to "direct-refund".
            append_sender (str, optional): The append sender option. Defaults to 'hosted'.

        Returns:
            dict: The status code and response of the API request.
        """

        payload = self._prepare_single_recipient_payload(sender=sender,
                                                         recipient=recipient,
                                                         body=body,
                                                         gateway=gateway,
                                                         append_sender=append_sender)

        return self._make_send_sms_request(payload=payload)

    def sendToMany(self, sender, recipients, body, gateway="direct-refund", append_sender='hosted'):
        """
        Sends an SMS to multiple recipients.

        Args:
            sender (str): The sender's name or number.
            recipients (list or tuple): The list of recipient phone numbers.
            body (str): The message content.
            gateway (str, optional): The gateway to use for sending the SMS. Defaults to "direct-refund".
            append_sender (str, optional): The append sender option. Defaults to 'hosted'.

        Returns:
            dict: The status code and response of the API request.
        """

        payload = self._prepare_multi_recipient_payload(sender=sender,
                                                        recipients=recipients,
                                                        body=body,
                                                        gateway=gateway,
                                                        append_sender=append_sender)

        return self._make_send_sms_request(payload=payload)

    def getWalletBalance(self):
        """
        Retrieves the wallet balance.

        Returns:
            dict: The status code and response of the API request.
        """

        return (self._make_sms_balance_request())

    def getDeliveryReport(self, message_id):
        """
        Retrieves the delivery report for a specific message.

        Args:
            message_id (str): The ID of the message.

        Returns:
            dict: The status code and response of the API request.
        """

        return self._make_delievery_report_request(message_id=message_id)

    def _validate_sender(self, sender):
        if not isinstance(sender, str):
            raise ValueError("Sender must be a string")

        if len(sender) > 11:
            raise ValueError("Sender max of 11 characters")

    def _validate_single_recipient(self, recipient):
        if not isinstance(recipient, str):
            raise ValueError("recipient must be a string")

        if len(recipient) > 13:
            raise ValueError("recipient max of 13 characters")

        if len(recipient) < 11:
            raise ValueError("recipient min of 11 characters")

        if len(recipient) != 13:
            raise ValueError(
                "recipient phone number should be 13 characters, should beginning with 234")

        if recipient[0:3] != "234":
            raise ValueError(
                "all recipients must be a nigerian number, should start with (234)")

    def _validate_many_recipients(self, recipients):
        if not isinstance(recipients, (list, tuple)):
            raise ValueError("recipients must be a list")

        for recipient in recipients:
            if len(recipient) > 13:
                raise ValueError("all recipients max of 13 characters")

            if not isinstance(recipient, str):
                raise ValueError("all recipients must be a string")

            if recipient[0:3] != "234":
                raise ValueError(
                    "all recipients must be a nigerian number, should start with (234)")

            if len(recipient) != 13:
                raise ValueError(
                    "recipient phone number should be 13 characters, should beginning with 234")

    def _validate_body(self, body):
        if not isinstance(body, str):
            raise ValueError("body must be a string")

    def _validate_gateway(self, gateway):
        valid_gateway = ['direct-refund', '1', 'direct-corporate',
                         '2', 'corporate', '6', 'international', '7', 'otp', '8']

        if gateway not in valid_gateway:
            raise ValueError(
                f"Invalid gateway, must be one of {valid_gateway}")

    def _validate_append_sender(self, append_sender):
        valid_append_sender = ['none', '1', 'hosted', '2', 'all', '3']

        if append_sender not in valid_append_sender:
            raise ValueError(
                f"Invalid Append Sender, must be one of {valid_append_sender}")

    def _validate_message_id(self, message_id):
        if not isinstance(message_id, str):
            raise ValueError("message_id must be a string")

    def _prepare_single_recipient_payload(self, sender, recipient, body, gateway, append_sender):

        self._validate_body(body)
        self._validate_sender(sender)
        self._validate_single_recipient(recipient)
        self._validate_gateway(gateway)
        self._validate_append_sender(append_sender)

        payload = {
            "body": body,
            "from": sender,
            "to": recipient,
            "api_token": self.api_token,
            "gateway": gateway,
            "append_sender": append_sender
        }
        return payload

    def _prepare_multi_recipient_payload(self, sender, recipients, body, gateway, append_sender):

        self._validate_body(body)
        self._validate_sender(sender)
        self._validate_many_recipients(recipients)
        self._validate_gateway(gateway)
        self._validate_append_sender(append_sender)

        recipients = ",".join(recipients)

        payload = {
            "body": body,
            "from": sender,
            "to": recipients,
            "api_token": self.api_token,
            "gateway": gateway,
            "append_sender": append_sender
        }
        return payload

    def _make_send_sms_request(self, payload):
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}

        req = requests.post(SEND_SMS_URL, json=payload, headers=headers)
        return {"status": req.status_code, "response": req.json()}

    def _make_sms_balance_request(self):
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}
        payload = {
            "api_token": self.api_token
        }

        req = requests.get(GET_SMS_BALANCE_URL, json=payload, headers=headers)
        return {"status": req.status_code, "response": req.json()}

    def _make_delievery_report_request(self, message_id):
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}

        self._validate_message_id(message_id)
        payload = {
            "api_token": self.api_token,
            "message_id": message_id
        }

        req = requests.get(GET_DELIVERY_REPORT_URL,
                           json=payload, headers=headers)
        return {"status": req.status_code, "response": req.json()}
