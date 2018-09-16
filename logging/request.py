import uuid
import time
import simplejson
import logging
from flask import current_app, request
from .models.log_request import LogRequest
from .models.log_entry import LogEntry


class CotRequest():
    def __init__(self):
        self.uuid = str(uuid.uuid4())
        self.log_object = LogRequest()
        self.epoch_start_ms = int(time.time() * 1000)
        self.log_max_level = 0
        self.log_counter = 0
        self.log_queue = []

        if 'COT_LOGGER_LEVEL' in current_app.config:
            self.log_level = current_app.config['COT_LOGGER_LEVEL']
        else:
            self.log_level = logging.DEBUG
        
        headers = []
        for h in request.headers:
            headers.append(h)

        form = []
        for f in request.form:
            form.append(f)
        if len(form) == 0:
            form = None

        self.log_object.create_new(
            container_uuid=current_app.config['cot_logging_container_uuid'],
            request_uuid=self.uuid,
            endpoint=request.endpoint,
            method=request.method,
            url=request.base_url,
            cookies=simplejson.dumps(request.cookies),
            headers=simplejson.dumps(headers),
            query_string=request.query_string,
            post=simplejson.dumps(form),
            data=request.get_data(as_text=True)
        )

    def get_uuid(self):
        return self.uuid

    def end(self, response):
        duration_ms = int(time.time() * 1000) - self.epoch_start_ms
        self.log_object.mark_complete(
          status_code=response.status_code,
          duration_ms=duration_ms,
          log_max_level=self.log_max_level
        )

    def debug(self, message, trace=None, code=None):
        if self.log_level <= logging.DEBUG:
            self.log(logging.DEBUG, message=message, trace=trace, code=code)

    def info(self, message, trace=None, code=None):
        if self.log_level <= logging.INFO:
            self.log(logging.INFO, message=message, trace=trace, code=code)

    def warning(self, message, trace=None, code=None):
        if self.log_level <= logging.WARNING:
            self.log(logging.WARNING, message=message, trace=trace, code=code)

    def error(self, message, trace=None, code=None):
        if self.log_level <= logging.ERROR:
            self.log(logging.ERROR, message=message, trace=trace, code=code)

    def critical(self, message, trace=None, code=None):
        if self.log_level <= logging.CRITICAL:
            self.log(logging.CRITICAL, message=message, trace=trace, code=code)

    def log(self, level, message, trace=None, code=None):
        entry = LogEntry(
                    request_uuid=self.uuid,
                    offset=int(time.time() * 1000) - self.epoch_start_ms,
                    level=level,
                    message=message,
                    trace=trace,
                    code=code
                )
                
    
