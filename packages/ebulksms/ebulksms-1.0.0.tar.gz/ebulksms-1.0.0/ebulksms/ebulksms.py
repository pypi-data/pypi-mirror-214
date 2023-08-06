import requests
import os
import json
import uuid

SEND_SMS_URL = "https://api.ebulksms.com:8080/sendsms.json"
DELIVERY_REPORTS_URL = "https://api.ebulksms.com:8080/getdlr.json?"
ACCOUNT_BALANCE_URL = "https://api.ebulksms.com:8080/balance"
GET_API_KEY_URL = "https://api.ebulksms.com:8080/getapikey.json"


class EBulkSMS:
    def __init__(self, api_token=None, email=None, password=None) -> None:
        """
        Initializes an instance of the EBulkSMS class.
        
        Using api_token and email
        >>> sms = EBulkSMS(api_token="<<Your API_Token>>", email=<<Your Email>>,)
        
        Using email and password
        >>> sms = EBulkSMS(email=<<Your Email>>, password=<<Your Password>>)

        Args:
            api_token (str): The API token for authenticating API requests.
            email (str): The email associated with the account.
            password (str): The password for the account.

        Raises:
            TypeError: If neither api_token and email nor email and password arguments are provided.
        """

        if api_token and email:
            self.api_token = api_token
            self.email = email

        elif email and password:
            self.api_token = self._get_api_token(
                email=email, password=password)
            self.email = email
        else:
            raise TypeError(
                "provide either an api_token and email or email and password arguments")

    def sendSMS(self, sender, recipients, message, flash=0, dndsender=1):
        """
        Sends an SMS message to one or more recipients.

        Args:
            sender (str): The sender ID or phone number.
            recipients (str, list, or tuple): The recipient(s) of the message. Can be a single phone number (str),
                or a list/tuple of phone numbers.
            message (str): The content of the message.
            flash (int, optional): Indicates whether the message is a flash message. Default is 0 (not a flash message).
            dndsender (int, optional): Indicates whether to deliver the message even if the recipient is on the
                Do-Not-Disturb (DND) list. Default is 1 (deliver to DND numbers).

        Returns:
            str: The JSON response containing the status of the sent message and related information.

        Raises:
            ValueError: If there was an error when sending the message.
        """

        data = self._prepare_json_payload(
            sender, recipients, message, flash, dndsender)

        response = self._make_send_sms_request(data["payload"])

        if self._can_convert_to_dict(response.text):
            dict_response = json.loads(response.text)
            if dict_response["response"]["status"] == "SUCCESS":
                dict_response["gsm"] = data["gsm"]
                return json.dumps(dict_response)
            else:
                status = dict_response["response"]["status"]
                error_response = f"Encounted an error when sending message: {status}"
                raise ValueError(error_response)
        else:
            error_response = f"Encounted an error when sending message: {response.text}"
            raise ValueError(error_response)

    def getBalance(self):
        """
        Retrieves the account balance.

        Returns:
            float: The account balance.

        Raises:
            ValueError: If there was an error when getting the balance.
        """

        url = f"{ACCOUNT_BALANCE_URL}/{self.email}/{self.api_token}"
        response = requests.get(
            url, headers={"Content-Type": "application/json"})
        balance = response.text
        if self._can_convert_to_float(balance):
            return float(balance)
        else:
            error_response = f"Encounted an error when getting the balance: {balance}"
            raise ValueError(error_response)

    def getDeliveryReport(self, unique_id):
        """
        Retrieves the delivery report for a specific message.

        Args:
            unique_id (str): The unique ID of the message.

        Returns:
            str: The JSON response containing the delivery report.

        Raises:
            ValueError: If there was an error when getting the delivery report.
        """
        url = f"{DELIVERY_REPORTS_URL}username={self.email}&apikey={self.api_token}&uniqueid={unique_id}"
        response = requests.get(
            url, headers={"Content-Type": "application/json"})

        if self._can_convert_to_dict(response.text):
            return response.text
        else:
            error_response = f"Encounted an error when getting the delivery report: {response.text}"
            raise ValueError(error_response)

    def _validate_sender(self, sender):
        if not isinstance(sender, str):
            raise ValueError("Sender must be a string")

        if len(sender) > 11:
            raise ValueError("Sender max of 11 characters")

    def _validate_recipients(self, recipients):
        if not isinstance(recipients, (list, tuple, str)):
            raise ValueError("recipients must be a string, list or tuple")

        if isinstance(recipients, (str)):
            if len(recipients) > 13:
                raise ValueError("recipient max of 13 characters")

            if len(recipients) < 11:
                raise ValueError("recipient min of 11 characters")

            if len(recipients) != 13:
                raise ValueError(
                    "recipient phone number should be 13 characters, should beginning with 234")

            if recipients[0:3] != "234":
                raise ValueError(
                    "all recipients must be a nigerian number, should start with (234)")
        else:
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
        if len(body) >= 600:
            raise ValueError("body character limit of 600 characters")

    def _validate_flash(self, flash):
        valid_flash = [0, 1]

        if flash not in valid_flash:
            raise ValueError(f"Invalid flash, must be one of {valid_flash}")

    def _validate_dndsender(self, dndsender):
        valid_dndsender = [0, 1]

        if dndsender not in valid_dndsender:
            raise ValueError(
                f"Invalid Append Sender, must be one of {valid_dndsender}")

    def _validate_unique_id(self, unique_id):
        if not isinstance(unique_id, str):
            raise ValueError("unique_id must be a string")

    def _prepare_json_payload(self, sender, recipients, message, flash, dndsender):
        self._validate_sender(sender)
        self._validate_recipients(recipients)
        self._validate_body(message)
        self._validate_flash(flash)
        self._validate_dndsender(dndsender)

        if isinstance(recipients, str):
            unique_id = self._generate_uuid()
            payload = {
                "SMS": {
                    "auth": {
                        "username": self.email,
                        "apikey": self.api_token
                    },
                    "message": {
                        "sender": sender,
                        "messagetext": message,
                        "flash": str(flash)
                    },
                    "recipients": {
                        "gsm": [
                            {
                                "msidn": recipients,
                                "msgid": unique_id
                            }
                        ]
                    },
                    "dndsender": dndsender
                }
            }
            return {"payload": payload, "gsm": [{
                "msidn": recipients,
                "msgid": unique_id
            }
            ]}
        else:
            gsm = [{"msidn": recipient, "msgid": self._generate_uuid()}
                   for recipient in recipients]
            payload = {
                "SMS": {
                    "auth": {
                        "username": self.email,
                        "apikey": self.api_token
                    },
                    "message": {
                        "sender": sender,
                        "messagetext": message,
                        "flash": str(flash)
                    },
                    "recipients": {
                        "gsm": gsm
                    },
                    "dndsender": dndsender
                }
            }
            return {"payload": payload, "gsm": gsm}

    def _generate_uuid(self):
        return str(uuid.uuid4())

    def _make_send_sms_request(self, payload):

        json_file_path = "./data.json"

        with open(json_file_path, "w") as file:
            file.write(json.dumps(payload))

        url = SEND_SMS_URL

        with open(json_file_path, "rb") as file:
            payload = file.read()

        response = requests.post(url, data=payload, headers={
                                 "Content-Type": "application/json"})

        os.remove(json_file_path)

        return response

    def _get_api_token(self, email, password):
        json_data = {
            "auth": {
                "username": email,
                "password": password
            }
        }

        json_file_path = "./data.json"

        with open(json_file_path, "w") as file:
            file.write(json.dumps(json_data))

        with open(json_file_path, "rb") as file:
            json_data = file.read()

        response = requests.post(GET_API_KEY_URL, data=json_data, headers={
                                 "Content-Type": "application/json"})

        os.remove(json_file_path)

        dict_response = json.loads(response.text)

        if dict_response["response"]["status"].lower() == "success":
            return dict_response["response"]["apikey"]
        else:
            error_response = dict_response["response"]["status"]
            raise ValueError(
                f"Encountered an error when fetching the api_token: {error_response}")

    def _can_convert_to_float(vself, variable):
        try:
            float(variable)
            return True
        except ValueError:
            return False

    def _can_convert_to_dict(self, json_variable):
        try:
            json.loads(json_variable)
            return True
        except ValueError:
            return False
