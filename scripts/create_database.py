"""
SQLALCHEMY_DATABASE_URI:
sqlite:////home/fconil/Progs/python/flask-installable-app/flaskapp/myflaskapp/app.db
"""

from sqlalchemy import create_engine

from myflaskapp.config import Config

from mymodels.base import MyBase

# If not imported these classes are not created
import mymodels.author  # noqa: F401

if __name__ == "__main__":
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

    MyBase.metadata.drop_all(engine)
    MyBase.metadata.create_all(engine)

    print(f"Database {Config.SQLALCHEMY_DATABASE_URI} is created.")
