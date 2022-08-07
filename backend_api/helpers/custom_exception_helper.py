from rest_framework import status
from rest_framework.exceptions import ErrorDetail, APIException
from rest_framework.views import exception_handler


def extract_message_from_data(data: [dict, list, tuple]):
    match type(data).__qualname__:
        case ErrorDetail.__qualname__:
            return str(data), data.code
        case list.__qualname__ | tuple.__qualname__:
            return extract_message_from_data(data[0])
        case _:
            return "error_not_found", "no_error"


def extract_message_code_from_exception(response: dict):
    for key in response:
        return extract_message_from_data(response[key])


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response_data = response.data
        message, code = extract_message_code_from_exception(response.data)
        response.data = {
            "error": {
                "data": response_data,
                "message": message,
                "code": code,
            }
        }
    return response


class CustomApiException(APIException):
    detail = None
    status_code = None

    # create constructor
    def __init__(self, message=None, status_code=None):
        # override public fields
        CustomApiException.status_code = status.HTTP_400_BAD_REQUEST if status_code is None else status_code
        CustomApiException.detail = message


class VerificationMailSentException(CustomApiException):
    pass


class AccountAlreadyVerifiedException(CustomApiException):
    pass


class VerificationTokenException(CustomApiException):
    pass


class UserBusinessNotFoundException(CustomApiException):
    pass
