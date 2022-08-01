from json_log_formatter import JSONFormatter
import json


class CustomJSONLoggerFormatter(JSONFormatter):
    def json_record(self, message, extra, record) -> dict:
        extra["level"] = record.levelname
        extra["module"] = record.module
        extra["funcName"] = record.funcName
        extra["lineno"] = record.lineno

        if "response_data" in extra:
            try:
                extra["response_data"] = json.loads(extra["response_data"].decode('utf8'))
            except:
                extra['response_data'] = extra["response_data"].decode('utf8')
        if "body" in extra:
            try:
                extra["body"] = json.loads(extra["body"].decode('utf8'))
            except:
                extra["body"] = extra["body"]
        return super(CustomJSONLoggerFormatter, self).json_record(message, extra, record)