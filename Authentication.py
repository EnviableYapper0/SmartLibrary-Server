import hmac
import os
from datetime import datetime, timedelta
from enum import Enum

from flask import request


class Permission(Enum):
    KIOSK = 1
    LIBRARIAN = 2


class Authentication:
    @staticmethod
    def validate_access():
        try:
            authentication_header = request.headers["Authorization"]
            request_timestamp = request.headers["Authorization-Timestamp"]
        except KeyError:
            return False

        request_datetime = datetime.fromtimestamp(float(request_timestamp))
        time_differences = datetime.now() - request_datetime

        if not authentication_header.startswith("hmac"):
            return False

        if time_differences > timedelta(minutes=10):
            return False

        authentication = authentication_header.split(' ')[1].split(':')
        client_id = int(authentication[0])
        digest = authentication[1]

        try:
            secret = Authentication.__get_client_secret(client_id)
        except KeyError:
            return False

        reconstructed_hmac = hmac.new(str.encode(secret), str.encode(request.path + '+' + request_timestamp), "sha3_256")

        authentication_successful = hmac.compare_digest(digest, reconstructed_hmac.hexdigest())

        if authentication_successful:
            return Permission(client_id)
        else:
            return False

    @staticmethod
    def __get_client_secret(client_id):
        if Permission(client_id) == Permission.KIOSK:
            return os.environ["KIOSK_SECRET"]
        elif Permission(client_id) == Permission.LIBRARIAN:
            return os.environ["LIBRARIAN_SECRET"]
        else:
            raise KeyError("Invalid Id")
