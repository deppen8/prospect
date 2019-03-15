
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class SimSession():
    """Object to handle setup/teardown as well as transactions for a SQLAlchemy `Session`

    Attributes
    ----------
    session : SQLAlchemy `Session`
    """

    def __init__(self, engine_str="sqlite:///simulation_default.db"):
        """Create `SimSession` instance

        Parameters
        ----------
        engine_str : str, optional
            Database URL (the default is "sqlite:///simulation_default.db")

        Notes
        -----
        The SQLAlchemy docs have some good examples of different types of database URLs. `https://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls <https://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls>`_
        """

        engine = create_engine(engine_str)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def stage(self, block):
        """Add a building block to the list of objects to save to the database

        """

        self.session.add(block)

    def unstage(self, block):
        """Remove a building block

        """

        self.session.expunge(block)

    def remove_from_db(self, block):

        self.session.delete(block)


# def start_session(SimSession()):
#     pass
