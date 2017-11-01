from sqlalchemy import (
    Column,
    Unicode,
    Float,
    DateTime,
    Integer
)

from .meta import Base
from datetime import datetime


class Posts(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    entry_title = Column(Unicode)
    body = Column(Unicode)
    creation_date = Column(DateTime)

    def __init__(self, *args, **kwargs):
        """Modify the init method to do more things."""
        super(Posts, self).__init__(*args, **kwargs)
        self.creation_date = datetime.now()

    def to_dict(self):
        """Take model attributes and render them as a dictionary."""
        return {
            'id': self.id,
            'entry_title': self.entry_title,
            'body': self.body,
            'creation_date': self.creation_date('%m/%d/%Y')
        }


# Index('my_index', MyModel.name, unique=True, mysql_length=255)
