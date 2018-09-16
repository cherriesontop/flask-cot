import uuid
from flask import g

from .logging.request import CotRequest


def cot_create_app(app):
    app.config['cot_logging_container_uuid'] = str(uuid.uuid4())


def cot_before_request():
    g.cot_request = CotRequest()
    g.id = g.cot_request.get_uuid()


def cot_after_request(response):
    for func in getattr(g, 'call_after_request', ()):
        response = func(response)
    g.cot_request.end(response)
    return response
    
