from flask_cot.db import db
from flask_cot.db.models import BaseModel


class LogEntryDb(db.Model):
    __bind_key__ = 'cot_logging'
    __abstract__ = True
    __base_tablename__ = 'cot_log_entries'
    id = db.Column(db.INTEGER(), primary_key=True, autoincrement=True)
    request_uuid = db.Column(db.CHAR(36), nullable=False, )
    offset = db.Column(db.INTEGER(), nullable=True)
    level = db.Column(db.INTEGER())
    code = db.Column(db.String)
    message = db.Column(db.String)
    trace = db.Column(db.String)

    def __repr__(self):
        return '<LogEntry %r %r %r >' %\
            self.id, self.request_id, self.message


class LogEntry(BaseModel):
    def __init__(
                self,
                request_uuid,
                offset,
                level,
                code,
                message,
                trace,
                save=True,
            ):
        super(LogEntry, self).__init__()
        self._db_model = self._get_db_model(LogEntryDb)
        self.reset()

        self.obj = self._db_model(
            request_uuid=request_uuid,
            offset=offset,
            level=level,
            code=code,
            message=message,
            trace=trace
        )
        if save:
            self.save()

    def save(self):
        #try:
        db.session.add(self.obj)
        db.session.commit()
        #except Exception:
        #    db.session.rollback()
