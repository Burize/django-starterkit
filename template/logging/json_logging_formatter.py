import os

from ddtrace.helpers import get_correlation_ids
from pythonjsonlogger.jsonlogger import JsonFormatter


class JsonLoggingFormatter(JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(JsonLoggingFormatter, self).add_fields(log_record, record, message_dict)

        # add dyno info
        dyno = os.getenv('DYNO')
        if dyno:
            log_record['dyno'] = dyno
            log_record['dynotype'] = dyno.split('.')[0]

        # add datadog trace variables
        trace_id, span_id = get_correlation_ids()
        log_record['dd.trace_id'] = trace_id or 0
        log_record['dd.span_id'] = span_id or 0

        # set logger name
        if not log_record.get('logger.name'):
            log_record['logger.name'] = record.name
