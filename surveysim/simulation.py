"""Handle creation of a simulation session

"""


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class SimSession():
    from .survey import Survey
    from .area import Area
    from .assemblage import Assemblage
    from .layer import Layer
    from .feature import Feature
    from .coverage import Coverage
    from .surveyunit import SurveyUnit
    from .team import Team
    from .surveyor import Surveyor

    def __init__(self, engine_str="sqlite:///simulation_default.db"):
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
