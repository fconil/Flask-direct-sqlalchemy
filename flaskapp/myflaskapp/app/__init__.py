from flask import Flask, Blueprint
from flask import current_app, _app_ctx_stack
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from myflaskapp.config import Config


bp = Blueprint("main", __name__)


def shutdown_session(response_or_exc):
    """Shutdown the session at the end of the request.
    """
    app = current_app._get_current_object()
    if app.config.get("SQLALCHEMY_COMMIT_ON_TEARDOWN", None):
        if response_or_exc is None:
            app.session.commit()

    app.session.remove()
    return response_or_exc


def create_app(config=Config):
    app = Flask(__name__)

    # Get database configuration
    app.config.from_object(config)

    # Technically, engine is just a connection pool to the database
    # One engine per applicationi ?
    app.engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

    # https://docs.sqlalchemy.org/en/13/orm/contextual.html#using-custom-created-scopes
    # The scoped_session object’s default behavior of “thread local”  is only
    # one of many options on how to “scope” a Session.
    # A custom scope can be defined based on any existing system of getting at
    # “the current thing we are working with”.
    app.session_factory = sessionmaker(bind=app.engine)
    app.session = scoped_session(app.session_factory, scopefunc=_app_ctx_stack)

    app.teardown_appcontext(shutdown_session)

    app.register_blueprint(bp)

    return app


from myflaskapp.app import routes  # noqa : E402, E401
