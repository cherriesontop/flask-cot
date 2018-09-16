import time
from flask_cot.db import db
from flask_cot.db.models import BaseModel


class LogRequestDb(db.Model):
    #def __init__(self):
    #    super(LogRequestDb, self).__init__()
    __abstract__ = True
    __base_tablename__ = 'cot_log_requests'
    __bind_key__ = 'cot_logging'
    
    id = db.Column(db.INTEGER(), primary_key=True, autoincrement=True)
    container_uuid = db.Column(db.CHAR(36))
    request_uuid = db.Column(db.CHAR(36))
    epoch_start = db.Column(db.INTEGER(), default=time.time)
    duration_ms = db.Column(db.INTEGER(), default=0)
    endpoint = db.Column(db.VARCHAR(50), default='Unknown')
    method = db.Column(db.VARCHAR(7), default='UNKNOWN')
    status_code = db.Column(db.CHAR(3), default='000')
    request_cookies = db.Column(db.TEXT(), default=None)
    request_headers = db.Column(db.TEXT(), default=None)
    request_query_string = db.Column(db.TEXT(), default=None)
    request_post = db.Column(db.TEXT(), default=None)
    request_data = db.Column(db.TEXT(), default=None)
    request_url = db.Column(db.VARCHAR(255), default=None)
    accounting_uuid = db.Column(db.CHAR(36))
    accounting_cost = db.Column(db.INTEGER(), default=1)
    accounting_code = db.Column(db.VARCHAR(45), default=None)
    log_max_level = db.Column(db.INTEGER(), default=0)
    
    def __repr__(self):
        return '<LogRequest id=%r>' % self.id


class LogRequest(BaseModel):
    def __init__(self, id=None):
        super(LogRequest, self).__init__()
        self._db_model = self._get_db_model(LogRequestDb)
        self.obj = None
        self.reset()
        if id:
            self.load(id)

    def create_new(
                self,
                container_uuid,
                request_uuid,
                endpoint,
                method,
                url,
                cookies=None,
                headers=None,
                query_string=None,
                post=None,
                data=None
                ):

        self.obj = self._db_model(
            container_uuid=str(container_uuid),
            request_uuid=str(request_uuid),
            endpoint=endpoint,
            method=method,
            request_headers=headers,
            request_cookies=cookies,
            request_query_string=query_string,
            request_post=post,
            request_data=data,
            request_url=url
        )
        try:
            db.session.add(self.obj)
            db.session.commit()
        except Exception:
            db.session.rollback()
            # TODO: distress

    def mark_complete(self, status_code, duration_ms, log_max_level):
        self.obj.duration_ms = duration_ms
        self.obj.status_code = str(status_code)
        self.log_max_level = log_max_level
        try:
            db.session.add(self.obj)
            db.session.commit()
        except Exception:
            db.session.rollback()
            # TODO: distress

    def update_accounting(self, uuid, cost, code):
        self.obj.accounting_uuid = str(uuid)
        self.obj.accounting_cost = cost
        self.obj.accounting_code = code
        try:
            db.session.add(self.obj)
            db.session.commit()
        except Exception:
            db.session.rollback()
            # TODO: distress
