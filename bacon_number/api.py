from collections import deque
from typing import Deque, Set, Tuple

from fastapi import FastAPI, HTTPException

from .graph import ActorsGraph
from .models import Actor, Session

"""Assumptions
- Users will search for their chosen actor to compare with Kevin Bacon using
the actors api
- The frontend will send the ID of the chosen actor to the API to get a
response
- The IDs of Actors are the IDs in the credits cast columns
- Each actor has a unique ID
- Actor IDs are integers
- If there is no link between 2 actors return an error and a message
"""

session = Session()
graph = ActorsGraph()
app = FastAPI()

KEVIN_BACON_ID = 4724


@app.get('/actors/{name}')
def get_actor(name: str):
    """API to return possible actors. Can be used in a dropdown that
    filters the backend based on the text entered

    Args:
        name (str): Name or partial name of the actor

    Raises:
        HTTPException: If actor cannot be found

    Returns:
        dictionary: Returns a object with key actors mapped to a list of actors
        E.g {
            actors: [
                { id: 4724, name: "Kevin Bacon" },
                { id: 1196258, name: "Kevin Bangos" },
                ...
            ]
        }
    """
    actors_match = (
        session.query(Actor)
        .filter(Actor.name.ilike(f'%{name}%'))
        .limit(10)
        .all()
    )
    if not actors_match:
        raise HTTPException(status_code=404, detail='Actor not found')
    return {'actors': actors_match}


@app.get('/degrees/{actor_id}')
def get_degrees(actor_id: int, degrees_to: int = KEVIN_BACON_ID):
    """API to return an actor degree from another. Comparison defaults to
    KEVIN_BACON_ID which is the ID for Kevin Bacon

    Args:
        actor_id (int): Actor's ID to start comparison
        degrees_to (int, optional): An optional actor ID to compare actor_id to.
        Defaults to KEVIN_BACON_ID.

    Raises:
        HTTPException: If actor cannot be found

    Returns:
        dictionary: Returns a dictionary with keys degree_no and info.
    """
    actors_check = {
        actor.id: actor.name
        for actor in
        session.query(Actor)
        .filter(Actor.id.in_([actor_id, degrees_to]))
        .all()
    }
    if len(actors_check) != 2 and actor_id != degrees_to:
        raise HTTPException(
            status_code=404,
            detail='One or both of actors do not exist',
        )

    pq: Deque[Tuple[int, int]] = deque([(actor_id, 1)])
    processed_actors: Set[int] = set()
    processed_movies: Set[int] = set()

    while pq:
        cur_actor_id, degree_no = pq.popleft()

        if (
            cur_actor_id in processed_actors or
            graph.actor_graph.get(actor_id) is None
        ):
            continue

        processed_actors.add(cur_actor_id)

        if cur_actor_id == degrees_to:
            return {
                'degree_no': degree_no,
                'info': (
                    f'{actors_check[actor_id]} is {degree_no} degree(s) from '
                    f'{actors_check[degrees_to]}'
                ),
            }

        for movie_id in graph.actor_graph[cur_actor_id]:
            if (
                movie_id in processed_movies or
                graph.movie_graph.get(movie_id) is None
            ):
                continue

            processed_movies.add(movie_id)

            for next_actor_id in graph.movie_graph[movie_id]:
                pq.append((next_actor_id, degree_no + 1))

    return {
        'degree_no': 0,
        'info': (
            f'{actors_check[actor_id]} has no link with '
            f'{actors_check[degrees_to]}'
        ),
    }
