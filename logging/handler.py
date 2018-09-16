import logging


class SQLAlchemyHandler(logging.Handler):
    def emit(self, record):
        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = traceback.format_exc(exc)

        path = request.path
        method = request.method
        ip = request.remote_addr

        log = Log(logger=record.__dict__['name'],
                  level=record.__dict__['levelname'],
                  trace=trace,
                  message=record.__dict__['msg'],
                  path=path,
                  method=method,
                  ip=ip,
                  is_admin=is_admin
        )
        db.session.add(log)
        db.session.commit()
