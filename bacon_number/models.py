from os import environ

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql.schema import ForeignKey

engine = create_engine(
    environ.get('DATABASE_URL', 'sqlite:///bacon.sql'),
    # echo=True,  # To debug queries
)

Session = sessionmaker(bind=engine)

Base = declarative_base()


class Actor(Base):
    """Actor's model

    Houses records of actors. IDs and names
    """
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(240), index=True, nullable=False)

    links = relationship('MovieLink', back_populates='actor')

    def __repr__(self) -> str:
        return f'<Actor {self.name} />'


class MovieLink(Base):
    """Movie cast's model

    Houses records of movie casts.
    movie_id is the credits ID for a movie
    actor_id is the actor's unique ID
    """
    __tablename__ = 'movie_links'

    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, index=True, nullable=False)
    actor_id = Column(
        Integer,
        ForeignKey('actors.id', onupdate="CASCADE", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    actor = relationship('Actor', back_populates='links')

    def __repr__(self) -> str:
        return f'<MovieLink {self.id} => {self.actor_id} />'
