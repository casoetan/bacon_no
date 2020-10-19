from collections import defaultdict
from typing import Dict, List, Set

from .models import MovieLink, Session

session = Session()


class ActorsGraph:
    def __init__(self) -> None:
        """Initialize in-memory data store with actors id and their
        relationship and movie cast with actors in the movie.

        This is run only when the server is started. This speeds up processing
        the degrees between actors and prevents the roundtrip between the
        application and the database
        """
        self.actor_graph: Dict[int, Set[int]] = defaultdict(set)
        self.movie_graph: Dict[int, Set[int]] = defaultdict(set)

        movie_credits: List[MovieLink] = session.query(MovieLink).all()

        self._process_graph(movie_credits)

    def _process_graph(self, movie_credits):
        """[Internal] Creates an adjacency list of actors and movie casts.

        This creates an adjacency list of actors to other actors they have
        worked directly with and an adjacency list of movie credits and
        cast in those movies

        Args:
            movie_credits (list): The database list of movie credits
        """
        for movie_credit in movie_credits:
            self.movie_graph[movie_credit.movie_id].add(movie_credit.actor_id)
            self.actor_graph[movie_credit.actor_id].add(movie_credit.movie_id)
