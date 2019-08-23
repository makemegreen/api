from contextlib import ContextDecorator
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Model = db.Model


class auto_close_db_transaction(ContextDecorator):
    def __enter__(self, *exc):
        pass

    def __exit__(self, *exc):
        if len(db.session.dirty) > 0:
            raise Exception('Session was left dirty')
        db.session.commit()
        return False
