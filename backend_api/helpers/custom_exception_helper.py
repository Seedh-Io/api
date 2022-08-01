from rest_framework.exceptions import ErrorDetail
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
