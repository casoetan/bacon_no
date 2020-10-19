import ast
import csv
from os import environ

from bacon_number.models import Actor, Base, MovieLink, Session, engine

"""
Assumptions
- Data is processed only once
- duplicate IDs are duplicate content
- credits csv has unique IDs for each movie as id
"""

session = Session()

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

actor_id_set = set()

file_path = environ.get('DATASET_FILE', './dataset/credits.csv')

# Pre process the CSVs and stores it in the database
with open(file_path) as f:
    movie_credits = csv.DictReader(f, delimiter=',')

    actors = []
    movie_links = []
    for movie_credit in movie_credits:
        movie_id = int(movie_credit['id'])
        casts = ast.literal_eval(movie_credit['cast'])

        for cast in casts:
            actor_id, actor_name = (
                cast['id'],
                cast['name'],
            )
            if actor_id not in actor_id_set:
                actor_id_set.add(actor_id)
                actor = Actor(id=actor_id, name=actor_name)
                actors.append(actor)

            movie = MovieLink(movie_id=movie_id, actor_id=actor_id)
            movie_links.append(movie)

    session.bulk_save_objects(actors)
    session.bulk_save_objects(movie_links)
    session.commit()

session.close()
