from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Unicode,
)

from .meta import Base
from datetime import datetime


class Entry(Base):
    """Creates a class Entry."""

    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    body = Column(Unicode)
    creation_date = Column(DateTime)

    def __init(self, *args, **kwargs):
        """Modify the init method to do new things."""
        super(Entry, self).__init__(*args, **kwargs)
        self.creation_date = datetime.now()

    def to_dict(self):
        """Take all model attributes and renders them as a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'creation_date': self.creation_date.strftime('%m/%d/%Y')
        }


# Index('my_index', MyModel.name, unique=True, mysql_length=255)
